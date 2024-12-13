# Casino Blockchain Project

This project is a blockchain-based system for processing and recovering transaction data for a casino. It includes both a backend and a frontend component to handle encryption, decryption, and user interactions.

## Project Overview

The Casino Blockchain Project consists of two main components:

1. **Backend**: Handles the encryption and decryption of transaction data, using secret sharing and encoding techniques.
2. **Frontend**: Provides a user interface for uploading transaction CSV files, downloading templates, and recovering encrypted data.

## Features

- **Transaction Processing**: Upload and process transaction CSV files.
- **Data Encryption**: Encrypt transaction data using secret sharing.
- **Data Recovery**: Recover original transaction data from encrypted files.
- **CSV Template**: Download a CSV template for transaction data.

## Prerequisites

- **Node.js**: Required for running the frontend.
- **Python**: Required for running the backend.
- **Flask**: Python web framework used in the backend.
- **Axios**: HTTP client used in the frontend for API requests.

## Setup Instructions

### Backend Setup

1. **Navigate to the Backend Directory**:
   ```bash
   cd casino-blockchain-backend
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend Server**:
   ```bash
   python SecretSharingAndEncoding.py
   ```

### Frontend Setup

1. **Navigate to the Frontend Directory**:
   ```bash
   cd casino-blockchain-frontend
   ```

2. **Install Node.js Dependencies**:
   ```bash
   npm install
   ```

3. **Run the Frontend Server**:
   ```bash
   npm start
   ```

## Usage

### Uploading Transactions

1. **Download the CSV Template**: Navigate to the "Upload Transaction CSV" section and download the template.
2. **Fill Out the Template**: Enter your transaction data into the CSV template.
3. **Upload the CSV File**: Use the file upload form to select and upload your completed CSV file.
4. **Process the File**: Click "Upload and Process" to send the file to the backend for processing.

### Recovering Transactions

1. **Upload Encrypted File and Keys**: Navigate to the "Recover Transaction CSV" section and upload the encrypted file along with the necessary key files.
2. **Recover Data**: Click "Recover and Download" to initiate the recovery process and download the recovered transaction data.

## File Structure

- **casino-blockchain-backend**: Contains backend scripts and logic for encryption and decryption.
  - `SecretSharingAndEncoding.py`: Main backend script.
  - `recovered_transaction.csv`: Example of a recovered transaction file.
  - `transaction_template.csv.enc.key`: Example key file for encryption.

- **casino-blockchain-frontend**: Contains React components for the user interface.
  - `src/components/FileUpload.js`: Component for uploading transaction CSV files.
  - `src/components/FileRecovery.js`: Component for recovering encrypted transaction data.

## Troubleshooting

- **Missing Files**: Ensure all required files (e.g., images for steganography) are available in the expected directories.
- **Server Errors**: Check the console logs for any error messages and ensure all dependencies are installed correctly.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [Your Name] at [Your Email].
