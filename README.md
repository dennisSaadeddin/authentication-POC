# Authentication API MVP

A lightweight, secure authentication API built with FastAPI, SQLAlchemy, and SQLite. This MVP provides basic user authentication functionality with JWT token-based security.

## Features

- User registration (signup)
- User authentication (login)
- JWT token-based authentication
- Async database operations
- Password hashing with bcrypt
- Input validation with Pydantic
- OpenAPI documentation (Swagger UI)
- Database migrations with Alembic

## Technical Stack

- **Framework**: FastAPI 0.104.0
- **ASGI Server**: Uvicorn 0.24.0
- **Database**: SQLite with async support
- **ORM**: SQLAlchemy 2.0.0 with async features
- **Migrations**: Alembic 1.12.0
- **Security**:
  - passlib 1.7.4 for password hashing
  - python-jose 3.3.0 for JWT handling
  - bcrypt 4.0.1 for password hashing algorithm
- **Environment**: python-dotenv 1.0.0
- **API Documentation**: Swagger UI (built into FastAPI)

## Project Structure

```
authentication-api/
├── alembic/                    # Database migrations
│   ├── versions/               # Migration versions
│   ├── env.py                  # Alembic environment config
│   └── script.py.mako         # Migration script template
├── app/
│   ├── api/
│   │   ├── auth.py            # Authentication endpoints
│   │   └── deps.py            # Dependencies
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   └── security.py        # Security utilities
│   ├── db/
│   │   ├── base.py            # Database base setup
│   │   └── session.py         # Database session management
│   ├── models/                 # SQLAlchemy models
│   │   └── user.py            # User model
│   └── schemas/               # Pydantic models
│       └── auth.py            # Authentication schemas
├── scripts/
│   ├── create_users.sh        # User creation script
│   └── view_users.py          # Database viewer script
├── .env                        # Environment variables
├── main.py                     # Application entry point
└── requirements.txt            # Project dependencies

```

## Setup Instructions

1. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (copy from .env.example):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the server:
   ```bash
   python main.py
   ```

The API will be available at:
- Main API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### 1. Signup (/api/signup)
- Method: POST
- Purpose: Create new user account
- Request Body:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- Response:
  ```json
  {
    "username": "string",
    "id": "integer",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```

### 2. Login (/api/login)
- Method: POST
- Purpose: Authenticate user and get JWT token
- Request Body:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- Response:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "message": "Successfully logged in!"
  }
  ```

## Security Features

1. **Password Security**:
   - Passwords are hashed using bcrypt
   - Salt is automatically handled by bcrypt
   - Work factor is configurable

2. **JWT Authentication**:
   - Tokens expire after configurable time
   - Uses HS256 algorithm
   - Includes user claims in payload

3. **Database Security**:
   - Async operations prevent blocking
   - Prepared statements prevent SQL injection
   - Input validation using Pydantic

## Testing

1. Create test users:
   ```bash
   ./create_users.sh
   ```

2. View database contents:
   ```bash
   python view_users.py
   ```

## Error Handling

The API provides clear error messages for:
- Invalid credentials
- Duplicate usernames
- Missing required fields
- Invalid token
- Expired token

## Development Tools

1. Database migrations:
   ```bash
   # Create new migration
   alembic revision --autogenerate -m "description"
   
   # Apply migrations
   alembic upgrade head
   
   # Rollback
   alembic downgrade -1
   ```

2. View logs:
   ```bash
   # Server logs
   python main.py
   
   # Database logs (set echo=True in session.py)
   ```

## Production Considerations

For production deployment:
1. Use a production-grade database (PostgreSQL recommended)
2. Set up proper CORS policies
3. Use HTTPS
4. Configure proper logging
5. Set up rate limiting
6. Use environment-specific configurations
7. Implement proper error tracking
8. Set up monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Building and Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/authentication-poc.git
   cd authentication-poc
   ```

2. Build and start the application:
   ```bash
   docker-compose up --build
   ```

3. The API will be available at:
   - Main API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Services

- **api**: The main FastAPI application
- **migrate**: Runs database migrations
- **test**: Runs test suite (optional)

### Environment Configuration

- The `.env` file is automatically generated during Docker build
- You can customize environment variables in the Dockerfile or docker-compose.yml

### Persistent Data

- Database files are stored in the `./data` directory
- Volumes are mapped to preserve data between container restarts

### Running Tests

```bash
docker-compose run test
```

### Stopping the Application

```bash
docker-compose down
```

### Production Considerations

- Replace the generated SECRET_KEY with a secure, persistent key
- Configure CORS settings in `main.py`
- Consider using a production-grade database
- Set up proper logging and monitoring

### Troubleshooting

- Ensure Docker and Docker Compose are installed
- Check container logs with `docker-compose logs`
- Verify network ports are not in use 