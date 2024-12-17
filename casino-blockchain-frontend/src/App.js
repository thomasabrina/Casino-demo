import React from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import FileRecovery from './components/RecoveryUpload';

function App() {
  return (
    <div className="App">
      <h1>Casino Data Processing System</h1>
      <FileUpload />
      <FileRecovery />
    </div>
  );
}

export default App;
