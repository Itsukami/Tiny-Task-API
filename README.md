# **Tiny Task API**

A robust, minimal REST API built with FastAPI and SQLite.  
Designed as a portfolio MVP demonstrating clean architecture, strict validation, and comprehensive testing.

## **Features**

* **FastAPI** for a clean, modern REST API. 
* **SQLite** (Standard Library) for lightweight persistence.  
* **Pydantic** for strict data validation (Schema enforcement).  
* **Pytest** for automated integration testing.  
* **Error Handling**: Standardized JSON error responses.  
* **Pagination**: Limit and Offset support on listing endpoint.

## **Project Structure**

tiny-task-api/  
├── app/  
│   ├── \_\_init\_\_.py \# Makes 'app' importable  
│   ├── main.py    \# Entry point & Endpoints  
│   ├── models.py  \# Pydantic Schemas  
│   └── db.py      \# Database connection handling  
├── tests/  
│   ├── \_\_init\_\_.py \# Makes 'tests' discoverable  
│   └── test\_tasks.py \# Integration tests  
├── requirements.txt  
└── README.md

## **Setup & Run**

### Prerequisties

* **Python3.12+** (Required due to dependencies like pydantic-core)

### **1\. Environment Setup**

**Mac / Linux:**

\# Create virtual environment  
python3 \-m venv venv

\# Activate virtual environment  
source venv/bin/activate

\# Install dependencies  
pip install \-r requirements.txt

**Windows:**

\# Create virtual environment  
python \-m venv venv

\# Activate virtual environment  
venv\\Scripts\\activate

\# Install dependencies  
pip install \-r requirements.txt

### **2\. Run Application**

The application handles database creation automatically on startup.  
We use python \-m to ensure the correct environment is used.  
python \-m uvicorn app.main:app \--reload

API will be available at: http://127.0.0.1:8000  
Documentation: http://127.0.0.1:8000/docs

### **3\. Run Tests**

Running via python \-m adds the current directory to the system path, preventing "Module Not Found" errors.

python \-m pytest \-v

## **API Usage Examples**

**Create Task**

curl \-X POST "http://127.0.0.1:8000/tasks" \
     \-H "Content-Type: application/json" \
     \-d '{"title": "Complete the challenge"}'

**List Tasks (with pagination)**

curl "http://127.0.0.1:8000/tasks?limit=10\&done=false"

**Update Task**

curl \-X PATCH "http://127.0.0.1:8000/tasks/1" \
     \-H "Content-Type: application/json" \  
     \-d '{"done": true}'

**Delete Task**

curl \-X DELETE "http://127.0.0.1:8000/tasks/1"  
