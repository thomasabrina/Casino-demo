import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import hashlib
import os
import pandas as pd
import logging
import reedsolo

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
logging.basicConfig(level=logging.DEBUG)

# Initialize Reed-Solomon codec
rs = reedsolo.RSCodec(10)  # 10 is the number of error correction symbols

@app.route('/api/process-transaction', methods=['POST'])
def process_transaction():
    print("Received a request to /api/process-transaction")
    output_dir = '/Users/lanxiangzhang/Desktop/Projects/Casino-demo/casino-blockchain-backend/out'
    if 'file' not in request.files:
        print("No file part in the request")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return jsonify({'error': 'No selected file'}), 400

    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, file.filename)
    try:
        file.save(file_path)
        print(f"File saved to {file_path}")
    except Exception as e:
        print(f"Failed to save file: {e}")
        return jsonify({'error': 'Failed to save file'}), 500

    try:
        df = pd.read_csv(file_path)
        print("CSV file read successfully")

        required_columns = ['Transaction ID', 'User ID', 'Amount', 'Date', 'Type', 'Game ID', 'Currency', 'Status', 'Payment Method', 'Notes']
        if not all(column in df.columns for column in required_columns):
            print("CSV file is missing required columns")
            return jsonify({'error': 'CSV file is missing required columns'}), 400

        start_time = time.time()
        try:
            # Ensure images directory exists
            images_dir = 'images'
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
                subprocess.run("stegosecrets images", shell=True, check=True)

            # Use stego CLI to encrypt the file
            result = subprocess.run(
                ['stego', 'encrypt', '--file', file_path, '--parts', '5', '--threshold', '3', '--output', output_dir],
                check=True, capture_output=True, text=True
            )
            print("Stego command output:", result.stdout)

            # Read the file content
            with open(file_path, 'rb') as f:
                file_content = f.read()

            # Encode data with Reed-Solomon
            encoded_data = rs.encode(file_content)
            with open('encoded_data.bin', 'wb') as f:
                f.write(encoded_data)

        except subprocess.CalledProcessError as e:
            print(f"Error during stego command execution: {e.stderr}")
            return jsonify({'error': 'Failed to process transaction with StegoSecrets'}), 500

        share_hashes = []
        for i in range(5):
            key_file = os.path.join(output_dir, f'{i+1:03}.key')
            if not os.path.exists(key_file):
                print(f"File not found: {key_file}")
                return jsonify({'error': f'File not found: {key_file}'}), 500
            with open(key_file, 'rb') as f:
                share = f.read()
                share_hash = hashlib.sha256(share).hexdigest()
                share_hashes.append(share_hash)

        processing_time = time.time() - start_time

        summary_data = {
            'Summary': ['Transactions Processed', 'Processing Time (seconds)', 'Shares Created'],
            'Value': [len(df), f"{processing_time:.2f}", len(share_hashes)]
        }
        summary_df = pd.DataFrame(summary_data)

        shares_df = pd.DataFrame({'share_hashes': share_hashes})
        result_df = pd.concat([shares_df, summary_df], ignore_index=True)

        shares_file_path = 'shares.csv'
        result_df.to_csv(shares_file_path, index=False)

        response = send_file(shares_file_path, as_attachment=True, download_name='shares.csv')
        response.headers['X-Transaction-Count'] = str(len(df))
        response.headers['X-Processing-Time'] = f"{processing_time:.2f}"
        response.headers['X-Share-Count'] = str(len(share_hashes))
        return response

    except pd.errors.EmptyDataError:
        print("CSV file is empty or invalid")
        return jsonify({'error': 'CSV file is empty or invalid'}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
    finally:
        for i in range(5):
            key_file = os.path.join(output_dir, f'{i+1:03}.key')
            if os.path.exists(key_file):
                try:
                    os.remove(key_file)
                    print(f"Removed key file: {key_file}")
                except Exception as e:
                    print(f"Failed to remove key file {key_file}: {e}")
            image_file = os.path.join(images_dir, f'{i+1}.jpg')
            if os.path.exists(image_file):
                try:
                    os.remove(image_file)
                    print(f"Removed image file: {image_file}")
                except Exception as e:
                    print(f"Failed to remove image file {image_file}: {e}")

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            except Exception as e:
                print(f"Failed to remove file {file_path}: {e}")

        if os.path.exists('uploaded_transaction.csv.enc'):
            try:
                os.remove('uploaded_transaction.csv.enc')
                print("Removed file: uploaded_transaction.csv.enc")
            except Exception as e:
                print(f"Failed to remove file uploaded_transaction.csv.enc: {e}")

        if os.path.exists('uploaded_transaction.csv.key'):
            try:
                os.remove('uploaded_transaction.csv.key')
                print("Removed file: uploaded_transaction.csv.key")
            except Exception as e:
                print(f"Failed to remove file uploaded_transaction.csv.key: {e}")

    logging.info("File processed successfully")
    return jsonify({'shares': share_hashes, 'processing_time': processing_time})

@app.route('/api/recover-transaction', methods=['POST'])
def recover_transaction():
    try:
        # Get the uploaded files
        encoded_file = request.files.get('file')
        encoded_file_path = 'encoded_data.bin'
        encoded_file.save(encoded_file_path)

        # Decode data with Reed-Solomon
        with open(encoded_file_path, 'rb') as f:
            encoded_data = f.read()

        # Decode the data
        decoded_data = rs.decode(encoded_data)

        # If rs.decode() returns more than one value, adjust accordingly
        if isinstance(decoded_data, tuple):
            decoded_data = decoded_data[0]  # Extract the first element if it's a tuple

        # Save the decoded data to a file
        recovered_file_path = 'recovered_transaction.csv'
        with open(recovered_file_path, 'wb') as f:
            f.write(decoded_data)

        # Return the recovered file
        return send_file(recovered_file_path, as_attachment=True, download_name='recovered_transaction.csv')

    except Exception as e:
        print(f"Error during recovery: {e}")
        return jsonify({'error': 'Failed to recover file'}), 500
    finally:
        # Clean up temporary files
        if os.path.exists(encoded_file_path):
            try:
                os.remove(encoded_file_path)
                print(f"Removed file: {encoded_file_path}")
            except Exception as e:
                print(f"Failed to remove file {encoded_file_path}: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)