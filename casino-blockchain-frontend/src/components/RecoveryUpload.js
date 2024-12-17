import React, { useState } from 'react';
import axios from 'axios';

function RecoveryUpload() {
  const [encodedFile, setEncodedFile] = useState(null);
  const [error, setError] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleEncodedFileChange = (event) => {
    setEncodedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!encodedFile) {
      setError('Please upload the encoded file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', encodedFile);

    setIsProcessing(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5001/api/recover-transaction', formData, {
        responseType: 'blob',
      });

      // Create a link to download the recovered file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'recovered_transaction.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error recovering transaction:', error);
      setError('Failed to recover transaction. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h1>Recover Transaction</h1>
      <form>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="encodedFile" style={{ display: 'block', marginBottom: '5px' }}>
            Encoded File:
          </label>
          <input type="file" id="encodedFile" onChange={handleEncodedFileChange} />
          <small style={{ display: 'block', marginTop: '5px', color: '#555' }}>
            Please upload the encoded file for recovery.
          </small>
        </div>
        <button type="button" onClick={handleSubmit} style={{ padding: '10px 20px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Recover
        </button>
      </form>
      {isProcessing && <p style={{ marginTop: '15px' }}>Processing...</p>}
      {error && <p style={{ color: 'red', marginTop: '15px' }}>{error}</p>}
    </div>
  );
}

export default RecoveryUpload; 