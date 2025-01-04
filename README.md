# Telegram Task Assignment Bot

A production-ready Telegram bot for managing and assigning tasks in groups, with a REST API for external integrations.

## Features

- **Admin Commands**
  - `/create_task @username task description` - Create and assign a task
  - `/list_all_tasks` - View all tasks and their status

- **User Commands**
  - `/list_tasks` - View your assigned tasks
  - `/update_status task_id status` - Update task status (pending/in_progress/completed)

- **REST API**
  - Get tasks by user
  - Get tasks by status
  - JWT authentication for API access

## Setup

1. **Prerequisites**
   - Python 3.11+
   - PostgreSQL database
   - Docker (for containerized deployment)

2. **Environment Variables**
   ```
   # Copy example env file
   cp .env.example .env
   
   # Configure these variables
   DATABASE_URL=postgresql://user:password@localhost:5432/taskbot
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   JWT_SECRET_KEY=your_secret_key_here
   ```

3. **Installation**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   # Initialize database
   alembic upgrade head
   ```

## Project Structure

```
telegram-task-bot/
├── src/
│   ├── api/          # REST API endpoints
│   ├── auth/         # Authentication logic
│   ├── bot/          # Telegram bot handlers
│   ├── db/           # Database models
│   └── services/     # Business logic
├── tests/            # Unit tests
├── Dockerfile        # Container configuration
└── requirements.txt  # Python dependencies
```

## API Documentation

### Authentication

All API endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Endpoints

#### Get User Tasks
```
GET /tasks/{user_id}

Response:
{
  "tasks": [
    {
      "id": 1,
      "description": "Complete report",
      "status": "in_progress"
    }
  ]
}
```

#### Get Tasks by Status
```
GET /tasks/status/{status}

Response:
{
  "tasks": [
    {
      "id": 1,
      "description": "Complete report",
      "assigned_to": 123456
    }
  ]
}
```

## Deployment

### Docker
```bash
# Build container
docker build -t task-bot .

# Run container
docker run -p 8080:8080 --env-file .env task-bot
```

### Cloud Deployment

The application is designed to run on:
- Google Cloud Run
- AWS Lambda
- Azure Functions

Choose the platform that best suits your needs and follow their respective deployment guides.

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
The project follows PEP 8 guidelines. Run linting:
```bash
flake8 src/
```

## Security

- JWT authentication for API access
- Admin-only task creation
- Database connection pooling
- Rate limiting on API endpoints
- HTTPS enforcement
- Secure storage of secrets using environment variables

## Error Handling

- Graceful handling of Telegram API errors
- Database transaction management
- Input validation
- Comprehensive error logging

## Monitoring

- Request logging
- Error tracking
- Performance metrics
- Database query monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License