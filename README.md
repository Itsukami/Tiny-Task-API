Tiny Task APIA robust, minimal REST API built with FastAPI and SQLite.
Designed as a portfolio MVP demonstrating clean architecture, strict validation, and comprehensive testing.
FeaturesFastAPI for high-performance Async I/O.SQLite (Standard Library) for lightweight persistence.
Pydantic for strict data validation (Schema enforcement).
Pytest for automated integration testing.
Error Handling: Standardized JSON error responses.
Pagination: Limit and Offset support on listing endpoint.
Project Structure
tiny-task-api/
├── app/
│   ├── main.py    # Entry point & Endpoints
│   ├── models.py  # Pydantic Schemas
│   └── db.py      # Database connection handling
├── tests/
│   └── test_tasks.py # Integration tests
├── requirements.txt
└── README.md
Setup & Run
1. 
Environment Setup Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
2. Run ApplicationThe application handles database creation automatically on startup.uvicorn app.main:app --reload
API will be available at: http://127.0.0.1:80003. Run Testspytest -v
API Usage ExamplesCreate Taskcurl -X POST "[http://127.0.0.1:8000/tasks](http://127.0.0.1:8000/tasks)" \
     -H "Content-Type: application/json" \
     -d '{"title": "Complete the HENNGE challenge"}'
List Tasks (with pagination)curl "[http://127.0.0.1:8000/tasks?limit=10&done=false](http://127.0.0.1:8000/tasks?limit=10&done=false)"
Update Taskcurl -X PATCH "[http://127.0.0.1:8000/tasks/1](http://127.0.0.1:8000/tasks/1)" \
     -H "Content-Type: application/json" \
     -d '{"done": true}'
Delete Taskcurl -X DELETE "[http://127.0.0.1:8000/tasks/1](http://127.0.0.1:8000/tasks/1)"
