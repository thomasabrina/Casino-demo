import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a CSV file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setIsProcessing(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5001/api/process-transaction', formData, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'processed_result.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();

    } catch (error) {
      console.error('Error processing file:', error);
      setError('Failed to process file. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h1>Upload Transaction CSV</h1>
      <a href="/transaction_template.csv" download style={{ display: 'block', marginBottom: '15px', color: '#007bff', textDecoration: 'none' }}>
        Download CSV Template
      </a>
      <form>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="transactionFile" style={{ display: 'block', marginBottom: '5px' }}>
            Transaction CSV File:
          </label>
          <input type="file" id="transactionFile" accept=".csv" onChange={handleFileChange} />
          <small style={{ display: 'block', marginTop: '5px', color: '#555' }}>
            Please upload a CSV file containing transaction data.
          </small>
        </div>
        <button type="button" onClick={handleSubmit} style={{ padding: '10px 20px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Upload and Process with Stego
        </button>
      </form>
      {isProcessing && <p style={{ marginTop: '15px' }}>Processing...</p>}
      {error && <p style={{ color: 'red', marginTop: '15px' }}>{error}</p>}
    </div>
  );
}

export default FileUpload; 