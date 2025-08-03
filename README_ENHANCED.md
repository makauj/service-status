# Collection Management System

A comprehensive web-based system for managing collections data with Excel upload capabilities, read-only enforcement, and audit trails.

## 🚀 Features

### Core Functionality

- **Excel File Upload**: Upload Excel files with automatic data processing
- **Business Logic Enforcement**:
  - If 3 columns (ID, Name, Contact) are filled → Record becomes read-only
  - If only 2 columns filled and one is ID → Record remains editable
  - Email column is ignored during import but can be added later
- **Multiple Collections per ID**: Support for multiple entries with the same ID
- **Read-Only Enforcement**: Database-level triggers prevent updates on read-only records
- **Audit Trail**: Track who updated what and when

### Web Interface

- **Modern React Frontend**: Clean, responsive UI
- **Drag & Drop Upload**: Easy Excel file upload
- **Advanced Filtering**: Filter by ID, read-only status, date ranges
- **Inline Editing**: Edit non-read-only records directly in the interface
- **Real-time Updates**: Automatic refresh after operations

### API Features

- **RESTful API**: FastAPI-based with automatic documentation
- **Comprehensive Endpoints**: CRUD operations, filtering, history views
- **Authentication**: Simple header-based user tracking
- **Error Handling**: Detailed error messages and validation

## 🏗️ Architecture

```script
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │ PostgreSQL DB   │
│   (Port 3000)   │◄──►│   (Port 8000)   │◄──►│   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone and Navigate**

   ```bash
   cd service_status
   ```

2. **Start the Application**

   ```bash
   docker-compose up --build
   ```

3. **Access the Application**
   - Frontend: <http://localhost:3000>
   - API Documentation: <http://localhost:8000/docs>
   - API Health Check: <http://localhost:8000/health>

### Local Development

1. **Backend Setup**

   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   export DATABASE_URL="postgresql://collection_user:collection_pass@localhost:5432/collection_db"
   
   # Start the API server
   uvicorn api_main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend Setup**

   ```bash
   cd frontend
   npm install
   npm start
   ```

## 📊 Database Schema

### Collections Table

```sql
CREATE TABLE collections (
    record_id SERIAL PRIMARY KEY,
    ID INTEGER NOT NULL,                    -- Foreign key to other tables
    Name VARCHAR(255),                      -- Person's name
    Email VARCHAR(255),                     -- Email (ignored during import)
    Contact VARCHAR(255),                   -- Contact information
    Date DATE DEFAULT CURRENT_DATE,         -- Collection date
    read_only BOOLEAN DEFAULT FALSE,       -- Read-only flag
    last_updated_by VARCHAR(255),          -- Audit: who updated
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Audit: when updated
);
```

### Database Triggers

- **Read-Only Enforcement**: Prevents updates on read-only records
- **Audit Trail**: Automatically updates `last_updated_at` and `last_updated_by`

## 📁 Project Structure

```script
service_status/
├── app/                          # Backend application
│   ├── models/                   # Database models
│   │   └── enhanced_collection.py
│   ├── utils/                    # Utility functions
│   │   └── excel_processor.py
│   ├── crud.py                   # Database operations
│   ├── schemas.py                # Pydantic schemas
│   ├── database.py               # Database configuration
│   └── cofig.py                  # Configuration settings
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── UploadForm.js
│   │   │   ├── TableView.js
│   │   │   └── EditForm.js
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
├── api_main.py                   # FastAPI application
├── docker-compose.yml            # Docker orchestration
├── Dockerfile                    # Backend Docker image
├── init.sql                      # Database initialization
└── requirements.txt              # Python dependencies
```

## 🔧 API Endpoints

### Core Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /upload/` - Upload Excel file
- `GET /collections/` - List collections (with filtering)
- `GET /collections/editable/` - List only editable collections
- `GET /collections/readonly/` - List only read-only collections
- `GET /collections/{record_id}` - Get specific collection
- `GET /collections/history/{ID}` - Get all collections for an ID
- `PUT /collections/{record_id}` - Update collection
- `DELETE /collections/{record_id}` - Delete collection

### Query Parameters

- `ID` - Filter by ID number
- `read_only` - Filter by read-only status (true/false)
- `skip` - Pagination offset
- `limit` - Pagination limit

### Headers

- `X-User` - Required for operations that modify data

## 📤 Excel Upload Format

### Required Columns

- `ID` - Integer identifier (required)
- `Name` - Person's name
- `Contact` - Contact information

### Optional Columns

- `Date` - Collection date (defaults to current date)
- `Collected` - Ignored during processing

### Business Rules

1. **Read-Only Records**: If ID, Name, and Contact are all filled → record becomes read-only
2. **Editable Records**: If only 2 columns filled and one is ID → record remains editable
3. **Email Handling**: Email column is ignored during import but can be added via API
4. **Multiple Entries**: Same ID can have multiple collection records

### Example Excel Format

| ID | Name | Contact | Date | Collected |
|----|------|---------|------|-----------|
| 1001 | John Doe | 0712345678 | 2024-01-15 | Yes |
| 1002 | Jane Smith | 0723456789 | | No |
| 1003 | | 0734567890 | 2024-01-17 | |

## 🎯 Usage Examples

### 1. Upload Excel File

```bash
curl -X POST "http://localhost:8000/upload/" \
  -H "X-User: admin" \
  -F "file=@collections.xlsx"
```

### 2. Get All Collections

```bash
curl "http://localhost:8000/collections/"
```

### 3. Get Editable Collections Only

```bash
curl "http://localhost:8000/collections/editable/"
```

### 4. Update a Collection

```bash
curl -X PUT "http://localhost:8000/collections/1" \
  -H "X-User: admin" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "Updated Name",
    "Email": "updated@example.com",
    "Contact": "0712345678"
  }'
```

### 5. Get Collection History

```bash
curl "http://localhost:8000/collections/history/1001"
```

## 🔒 Security Features

- **Read-Only Enforcement**: Database triggers prevent unauthorized updates
- **Audit Trail**: Complete tracking of all changes
- **Input Validation**: Comprehensive validation of all inputs
- **Error Handling**: Detailed error messages without exposing internals

## 🧪 Testing

### API Testing

```bash
# Test the API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

### Frontend Testing

```bash
cd frontend
npm test
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**

   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   
   # View logs
   docker-compose logs db
   ```

2. **Upload Fails**
   - Ensure Excel file has required columns (ID, Name, Contact)
   - Check file format (.xlsx or .xls)
   - Verify file is not corrupted

3. **Frontend Can't Connect to API**
   - Check if backend is running on port 8000
   - Verify CORS settings
   - Check browser console for errors

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

## 🔄 Development

### Adding New Features

1. Update database schema in `init.sql`
2. Modify SQLAlchemy models in `app/models/`
3. Update Pydantic schemas in `app/schemas.py`
4. Add CRUD operations in `app/crud.py`
5. Create API endpoints in `api_main.py`
6. Update frontend components as needed

### Code Style

- Python: Follow PEP 8
- JavaScript: Use ESLint configuration
- SQL: Use consistent formatting

## 📈 Performance

### Optimizations

- Database indexes on frequently queried columns
- Connection pooling for database connections
- Gzip compression for API responses
- Static asset caching in nginx

### Monitoring

- Health check endpoints
- Database connection monitoring
- API response time tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:

- Check the API documentation at `/docs`
- Review the logs for error details
- Create an issue with detailed information
