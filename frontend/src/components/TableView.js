import React, { useState, useMemo } from 'react';
import './TableView.css';

const TableView = ({ collections, loading, onRefresh }) => {
  const [filterID, setFilterID] = useState('');
  const [filterReadOnly, setFilterReadOnly] = useState('all');
  const [sortBy, setSortBy] = useState('record_id');
  const [sortOrder, setSortOrder] = useState('desc');

  const filteredAndSortedCollections = useMemo(() => {
    let filtered = collections;

    // Filter by ID
    if (filterID) {
      filtered = filtered.filter(c => c.id.toString().includes(filterID));
    }

    // Filter by read-only status
    if (filterReadOnly !== 'all') {
      const isReadOnly = filterReadOnly === 'true';
      filtered = filtered.filter(c => c.read_only === isReadOnly);
    }

    // Sort
    filtered.sort((a, b) => {
      let aVal = a[sortBy];
      let bVal = b[sortBy];

      // Handle null values
      if (aVal === null) aVal = '';
      if (bVal === null) bVal = '';

      // Convert to string for comparison
      aVal = aVal.toString().toLowerCase();
      bVal = bVal.toString().toLowerCase();

      if (sortOrder === 'asc') {
        return aVal.localeCompare(bVal);
      } else {
        return bVal.localeCompare(aVal);
      }
    });

    return filtered;
  }, [collections, filterID, filterReadOnly, sortBy, sortOrder]);

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
  };

  const getSortIcon = (column) => {
    if (sortBy !== column) return '↕';
    return sortOrder === 'asc' ? '↑' : '↓';
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString();
  };

  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return '-';
    return new Date(dateTimeString).toLocaleString();
  };

  if (loading) {
    return (
      <div className="table-view">
        <div className="loading">Loading collections...</div>
      </div>
    );
  }

  return (
    <div className="table-view">
      <div className="table-header">
        <h2>Collections ({filteredAndSortedCollections.length})</h2>
        <button onClick={onRefresh} className="refresh-button">
          Refresh
        </button>
      </div>

      <div className="filters">
        <div className="filter-group">
          <label>Filter by ID:</label>
          <input
            type="text"
            value={filterID}
            onChange={(e) => setFilterID(e.target.value)}
            placeholder="Enter ID..."
          />
        </div>
        <div className="filter-group">
          <label>Filter by Status:</label>
          <select
            value={filterReadOnly}
            onChange={(e) => setFilterReadOnly(e.target.value)}
          >
            <option value="all">All</option>
            <option value="false">Editable</option>
            <option value="true">Read-Only</option>
          </select>
        </div>
      </div>

      <div className="table-container">
        <table className="collections-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('record_id')}>
                Record ID {getSortIcon('record_id')}
              </th>
                             <th onClick={() => handleSort('id')}>
                 ID {getSortIcon('id')}
               </th>
               <th onClick={() => handleSort('name')}>
                 Name {getSortIcon('name')}
               </th>
               <th onClick={() => handleSort('contact')}>
                 Contact {getSortIcon('contact')}
               </th>
               <th onClick={() => handleSort('email')}>
                 Email {getSortIcon('email')}
               </th>
               <th onClick={() => handleSort('date')}>
                 Date {getSortIcon('date')}
               </th>
              <th onClick={() => handleSort('read_only')}>
                Status {getSortIcon('read_only')}
              </th>
              <th onClick={() => handleSort('last_updated_at')}>
                Last Updated {getSortIcon('last_updated_at')}
              </th>
            </tr>
          </thead>
          <tbody>
            {filteredAndSortedCollections.map((collection) => (
              <tr 
                key={collection.record_id}
                className={collection.read_only ? 'read-only' : 'editable'}
              >
                                 <td>{collection.record_id}</td>
                 <td>{collection.id}</td>
                 <td>{collection.name || '-'}</td>
                 <td>{collection.contact || '-'}</td>
                 <td>{collection.email || '-'}</td>
                 <td>{formatDate(collection.date)}</td>
                <td>
                  <span className={`status ${collection.read_only ? 'read-only' : 'editable'}`}>
                    {collection.read_only ? 'Read-Only' : 'Editable'}
                  </span>
                </td>
                <td>{formatDateTime(collection.last_updated_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredAndSortedCollections.length === 0 && (
        <div className="no-data">
          {collections.length === 0 ? 'No collections found' : 'No collections match the current filters'}
        </div>
      )}
    </div>
  );
};

export default TableView; 