# Knowledge Base System

A company internal knowledge base system with RAG-powered Q&A capabilities.

## Features

- Document management (CRUD operations)
- Category and tag organization
- Full-text search
- RAG-powered Q&A with RAGFlow integration
- User authentication (to be implemented)
- Version history (to be implemented)

## Tech Stack

### Frontend
- Vue 3 + Vite
- Vue Router
- Pinia (state management)
- Axios (HTTP client)

### Backend
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL (database)
- RAGFlow (RAG engine)

### Infrastructure
- Docker & Docker Compose
- PostgreSQL 15
- RAGFlow

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd knowledge-base
   ```

2. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - RAGFlow: http://localhost:9380

## Development

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Project Structure

```
├── frontend/              # Vue.js frontend
│   ├── src/
│   │   ├── assets/       # Static assets
│   │   ├── router/       # Vue Router configuration
│   │   ├── views/        # Page components
│   │   └── main.js       # Entry point
│   ├── package.json
│   └── vite.config.js
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration
│   │   ├── crud/         # Database operations
│   │   ├── db/           # Database setup
│   │   ├── models/       # SQLAlchemy models
│   │   └── schemas/      # Pydantic schemas
│   ├── main.py
│   └── requirements.txt
├── docs/                  # Documentation
├── docker-compose.yml     # Docker services
└── README.md
```

## API Endpoints

### Documents
- `GET /api/v1/documents/` - List documents
- `POST /api/v1/documents/` - Create document
- `GET /api/v1/documents/{id}` - Get document
- `PUT /api/v1/documents/{id}` - Update document
- `DELETE /api/v1/documents/{id}` - Delete document

### Q&A
- `POST /api/v1/qa/ask` - Ask a question

## Configuration

Create a `.env` file in the backend directory:

```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=knowledge_base
SECRET_KEY=your_secret_key_here
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.