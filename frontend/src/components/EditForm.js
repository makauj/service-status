import React, { useState } from 'react';
import axios from 'axios';
import './EditForm.css';

const EditForm = ({ collections, onUpdate }) => {
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState({});
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const handleEdit = (collection) => {
    setEditingId(collection.record_id);
    setEditData({
      Name: collection.Name || '',
      Email: collection.Email || '',
      Contact: collection.Contact || '',
      Date: collection.Date ? new Date(collection.Date).toISOString().split('T')[0] : ''
    });
    setError(null);
  };

  const handleCancel = () => {
    setEditingId(null);
    setEditData({});
    setError(null);
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);

    try {
      await axios.put(`/collections/${editingId}`, editData);
      setEditingId(null);
      setEditData({});
      onUpdate(); // Refresh the data
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update collection');
      console.error('Update error:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleInputChange = (field, value) => {
    setEditData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString();
  };

  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return '-';
    return new Date(dateTimeString).toLocaleString();
  };

  return (
    <div className="edit-form">
      <div className="edit-header">
        <h2>Edit Collections</h2>
        <p>Only editable collections are shown here. Read-only collections cannot be modified.</p>
      </div>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      <div className="editable-collections">
        {collections.length === 0 ? (
          <div className="no-editable">
            <p>No editable collections found.</p>
            <p>Collections become editable when only 2 columns (including ID) are filled in the Excel file.</p>
          </div>
        ) : (
          <div className="collections-list">
            {collections.map((collection) => (
              <div key={collection.record_id} className="collection-item">
                {editingId === collection.record_id ? (
                  <div className="edit-mode">
                    <div className="edit-fields">
                      <div className="field-group">
                        <label>ID:</label>
                        <span className="readonly-field">{collection.ID}</span>
                      </div>
                      <div className="field-group">
                        <label>Name:</label>
                        <input
                          type="text"
                          value={editData.Name}
                          onChange={(e) => handleInputChange('Name', e.target.value)}
                          placeholder="Enter name..."
                        />
                      </div>
                      <div className="field-group">
                        <label>Email:</label>
                        <input
                          type="email"
                          value={editData.Email}
                          onChange={(e) => handleInputChange('Email', e.target.value)}
                          placeholder="Enter email..."
                        />
                      </div>
                      <div className="field-group">
                        <label>Contact:</label>
                        <input
                          type="text"
                          value={editData.Contact}
                          onChange={(e) => handleInputChange('Contact', e.target.value)}
                          placeholder="Enter contact..."
                        />
                      </div>
                      <div className="field-group">
                        <label>Date:</label>
                        <input
                          type="date"
                          value={editData.Date}
                          onChange={(e) => handleInputChange('Date', e.target.value)}
                        />
                      </div>
                    </div>
                    <div className="edit-actions">
                      <button 
                        onClick={handleSave} 
                        disabled={saving}
                        className="save-button"
                      >
                        {saving ? 'Saving...' : 'Save'}
                      </button>
                      <button onClick={handleCancel} className="cancel-button">
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="view-mode">
                    <div className="collection-info">
                      <div className="info-row">
                        <span className="label">Record ID:</span>
                        <span className="value">{collection.record_id}</span>
                      </div>
                      <div className="info-row">
                        <span className="label">ID:</span>
                        <span className="value">{collection.ID}</span>
                      </div>
                      <div className="info-row">
                        <span className="label">Name:</span>
                        <span className="value">{collection.Name || '-'}</span>
                      </div>
                      <div className="info-row">
                        <span className="label">Email:</span>
                        <span className="value">{collection.Email || '-'}</span>
                      </div>
                      <div className="info-row">
                        <span className="label">Contact:</span>
                        <span className="value">{collection.Contact || '-'}</span>
                      </div>
                      <div className="info-row">
                        <span className="label">Date:</span>
                        <span className="value">{formatDate(collection.Date)}</span>
                      </div>
                      <div className="info-row">
                        <span className="label">Last Updated:</span>
                        <span className="value">{formatDateTime(collection.last_updated_at)}</span>
                      </div>
                    </div>
                    <div className="view-actions">
                      <button 
                        onClick={() => handleEdit(collection)}
                        className="edit-button"
                      >
                        Edit
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default EditForm; 