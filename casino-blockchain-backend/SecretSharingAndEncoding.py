import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import hashlib
import os
import pandas as pd
import logging
import random

app = Flask(__name__)

# Allow CORS for requests from the frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

logging.basicConfig(level=logging.DEBUG)

def shamir_split(secret, parts, threshold):
    # Generate random coefficients for the polynomial
    coeffs = [random.randint(0, 256) for _ in range(threshold - 1)]
    coeffs.append(secret)

    # Generate shares
    shares = []
    for i in range(1, parts + 1):
        share = sum([coeff * (i ** exp) for exp, coeff in enumerate(coeffs)]) % 257
        shares.append((i, share))
    return shares

def vss_split(secret, parts, threshold):
    shares = shamir_split(secret, parts, threshold)
    commitments = [hashlib.sha256(str(share).encode()).hexdigest() for share in shares]
    return shares, commitments

def vss_verify(shares, commitments):
    for share, commitment in zip(shares, commitments):
        if hashlib.sha256(str(share).encode()).hexdigest() != commitment:
            return False
    return True

@app.route('/api/process-transaction', methods=['POST'])
def process_transaction():
    print("Received a request to /api/process-transaction")

    # Define the output directory at the start of the function
    output_dir = '/Users/lanxiangzhang/Desktop/Projects/Casino-demo/casino-blockchain-backend/out'

    if 'file' not in request.files:
        print("No file part in the request")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return jsonify({'error': 'No selected file'}), 400

    # Ensure the uploads directory exists
    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Save the uploaded file
    file_path = os.path.join(upload_dir, file.filename)
    try:
        file.save(file_path)
        print(f"File saved to {file_path}")
    except Exception as e:
        print(f"Failed to save file: {e}")
        return jsonify({'error': 'Failed to save file'}), 500

    # Validate and process the CSV file
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        print("CSV file read successfully")

        # Validate required columns
        required_columns = ['Transaction ID', 'User ID', 'Amount', 'Date', 'Type', 'Game ID', 'Currency', 'Status', 'Payment Method', 'Notes']
        if not all(column in df.columns for column in required_columns):
            print("CSV file is missing required columns")
            return jsonify({'error': 'CSV file is missing required columns'}), 400

        # Use StegoSecrets CLI to encrypt and split the secret
        start_time = time.time()
        try:
            result = subprocess.run(['stego', 'encrypt', '--file', file_path, '--parts', '5', '--threshold', '3'], check=True, capture_output=True, text=True)
            print("Stego command output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error during stego command execution: {e.stderr}")
            return jsonify({'error': 'Failed to process transaction with StegoSecrets'}), 500

        # Wait for files to be created
        time.sleep(1)  # Adjust the sleep time as necessary

        # Create a new CSV file with share hashes
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

        # Create a DataFrame for the shares
        shares_df = pd.DataFrame({'share_hashes': share_hashes})

        # Calculate processing time
        processing_time = time.time() - start_time

        # Add summary information to the DataFrame
        summary_data = {
            'Summary': ['Transactions Processed', 'Processing Time (seconds)', 'Shares Created'],
            'Value': [len(df), f"{processing_time:.2f}", len(share_hashes)]
        }
        summary_df = pd.DataFrame(summary_data)

        # Concatenate the summary with the shares data
        result_df = pd.concat([shares_df, summary_df], ignore_index=True)

        # Save the result to a CSV file
        shares_file_path = 'shares.csv'
        result_df.to_csv(shares_file_path, index=False)

        # Return the CSV file as a response
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
        # Clean up temporary files
        for i in range(5):
            key_file = os.path.join(output_dir, f'{i+1:03}.key')
            if os.path.exists(key_file):
                try:
                    os.remove(key_file)
                    print(f"Removed key file: {key_file}")
                except Exception as e:
                    print(f"Failed to remove key file {key_file}: {e}")
            else:
                print(f"Key file not found: {key_file}")

            # Ensure the image files are also removed if they exist
            image_file = f'{i+1}.jpg'
            if os.path.exists(image_file):
                try:
                    os.remove(image_file)
                    print(f"Removed image file: {image_file}")
                except Exception as e:
                    print(f"Failed to remove image file {image_file}: {e}")
            else:
                print(f"Image file not found: {image_file}")

        # Ensure the encrypted file and key are removed if they exist
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
        encrypted_file = request.files.get('file')
        keys = request.files.getlist('keys')

        # Save the uploaded files temporarily
        encrypted_file_path = 'uploaded_transaction.enc'
        encrypted_file.save(encrypted_file_path)

        key_paths = []
        for key in keys:
            key_path = key.filename
            key.save(key_path)
            key_paths.append(key_path)

        # Example decryption logic (replace with your actual logic)
        # This is a placeholder for the actual decryption command
        # os.system(f"your_decryption_command --key {key_path} --file {encrypted_file_path}")

        # Simulate recovery process
        recovered_file_path = 'recovered_transaction.csv'
        with open(recovered_file_path, 'w') as f:
            f.write("Transaction ID,User ID,Amount,Date,Type,Game ID,Currency,Status,Payment Method,Notes\n")
            f.write("1,123,100,2024-12-11,Deposit,456,USD,Completed,Credit Card,Test transaction\n")

        # Return the recovered file
        return send_file(recovered_file_path, as_attachment=True, download_name='recovered_transaction.csv')

    except Exception as e:
        print(f"Error during recovery: {e}")
        return jsonify({'error': 'Failed to recover file'}), 500

@app.route('/api/process-transaction-vss', methods=['POST'])
def process_transaction_vss():
    print("Received a request to /api/process-transaction-vss")
    # ... common file handling and validation code ...

    try:
        # Example secret for demonstration purposes
        secret = int.from_bytes(os.urandom(32), byteorder='big')
        shares, commitments = vss_split(secret, parts=5, threshold=3)

        # Verify shares
        if not vss_verify(shares[:3], commitments[:3]):
            return jsonify({'error': 'Share verification failed'}), 400

        # Process shares and create response
        share_hashes = [hashlib.sha256(str(share).encode()).hexdigest() for share in shares]
        return jsonify({'shares': share_hashes, 'commitments': commitments})

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
