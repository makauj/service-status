import React, { useState, useEffect } from 'react';
import './App.css';
import UploadForm from './components/UploadForm';
import TableView from './components/TableView';
import EditForm from './components/EditForm';
import axios from 'axios';

// Configure axios defaults
axios.defaults.headers.common['X-User'] = 'admin_user'; // Replace with actual user management

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchCollections = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('/collections/');
      setCollections(response.data);
    } catch (err) {
      setError('Failed to fetch collections');
      console.error('Error fetching collections:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCollections();
  }, []);

  const handleUploadSuccess = () => {
    fetchCollections(); // Refresh the table after upload
    setActiveTab('view');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Collection Management System</h1>
        <nav className="nav-tabs">
          <button 
            className={activeTab === 'upload' ? 'active' : ''} 
            onClick={() => setActiveTab('upload')}
          >
            Upload Excel
          </button>
          <button 
            className={activeTab === 'view' ? 'active' : ''} 
            onClick={() => setActiveTab('view')}
          >
            View Collections
          </button>
          <button 
            className={activeTab === 'edit' ? 'active' : ''} 
            onClick={() => setActiveTab('edit')}
          >
            Edit Collections
          </button>
        </nav>
      </header>

      <main className="App-main">
        {error && (
          <div className="error-message">
            {error}
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        {activeTab === 'upload' && (
          <UploadForm onUploadSuccess={handleUploadSuccess} />
        )}

        {activeTab === 'view' && (
          <TableView 
            collections={collections} 
            loading={loading} 
            onRefresh={fetchCollections}
          />
        )}

        {activeTab === 'edit' && (
          <EditForm 
            collections={collections.filter(c => !c.read_only)} 
            onUpdate={fetchCollections}
          />
        )}
      </main>
    </div>
  );
}

export default App; 