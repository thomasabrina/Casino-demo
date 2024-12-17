# Casino Blockchain Project

This project is an online casino transaction processing system that utilizes advanced security techniques, including Reed-Solomon encoding and Stego, to enhance data integrity and confidentiality. It consists of a frontend built with React and a backend powered by Flask.

## Project Structure

- **casino-blockchain-frontend**: The frontend application built with React, providing an intuitive interface for users to upload and recover transaction files.
- **casino-blockchain-backend**: The backend application built with Flask, handling secure transaction processing and recovery.

## Features

- **Transaction Processing**: Upload and process transaction CSV files with enhanced security.
- **Data Encoding and Concealment**: Use Reed-Solomon encoding and Stego for robust data handling and concealment.
- **Download Results**: Download processed and recovered transaction files.

## Prerequisites

- Node.js and npm (for the frontend)
- Python 3.x (for the backend)
- Flask and Flask-CORS
- Pandas
- Axios (for making HTTP requests in the frontend)
- Reed-Solomon and Stego libraries

## Setup Instructions

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd casino-blockchain-backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask application**:
   ```bash
   python SecretSharingAndEncoding.py
   ```

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd casino-blockchain-frontend
   ```

2. **Install the dependencies**:
   ```bash
   npm install
   ```

3. **Start the React application**:
   ```bash
   npm start
   ```

## Usage

1. **Access the application**: Open your web browser and go to `http://localhost:3000`.

2. **Upload a CSV file**: Use the file input to upload a transaction CSV file.

3. **Process the file**: Click the appropriate button to process the file using Reed-Solomon encoding and Stego.

4. **Download the results**: After processing, use the download buttons to retrieve the result CSV files.

## File Structure

- **casino-blockchain-frontend/src/components/FileUpload.js**: Handles file uploads and interactions with the backend.
- **casino-blockchain-frontend/src/components/RecoveryUpload.js**: Manages the recovery of transaction files.
- **casino-blockchain-backend/SecretSharingAndEncoding.py**: Contains the Flask routes and logic for processing and recovering transactions.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
