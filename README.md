# Casino Blockchain Project

This project is an online casino transaction processing system that utilizes secret sharing algorithms to enhance security. It consists of a frontend built with React and a backend powered by Flask.

## Project Structure

- **casino-blockchain-frontend**: The frontend application built with React.
- **casino-blockchain-backend**: The backend application built with Flask.

## Features

- **Transaction Processing**: Upload and process transaction CSV files.
- **Secret Sharing**: Use Shamir's Secret Sharing and Verifiable Secret Sharing (VSS) to securely distribute sensitive information.
- **Download Results**: Download the processed results as CSV files for each algorithm.

## Prerequisites

- Node.js and npm (for the frontend)
- Python 3.x (for the backend)
- Flask and Flask-CORS
- Pandas
- Axios (for making HTTP requests in the frontend)

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

3. **Process the file**: Click the appropriate button to process the file using either Shamir's Secret Sharing or VSS.

4. **Download the results**: After processing, use the download buttons to retrieve the result CSV files for each algorithm.

## File Structure

- **casino-blockchain-frontend/src/components/FileUpload.js**: Handles file uploads and interactions with the backend.
- **casino-blockchain-backend/SecretSharingAndEncoding.py**: Contains the Flask routes and logic for processing transactions and secret sharing.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
