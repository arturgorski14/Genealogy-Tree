# 🌳 Genealogy-Tree

Graph-based genealogy tree.

## 🧠 Technologies
Neo4j – graph database for representing people and relationships

FastAPI – REST API for interacting with the backend (in progress)

React – frontend UI for displaying the tree (in progress)

pytest – for ensuring reliability

poetry - for managing packages

---

## ⚙️ Prerequisites
- Install Neo4j: [neo4j.com/download](https://neo4j.com/download/)
- Start **Neo4j Desktop** and create a database  
  (this project was created on 5.24.0, but any version should work)
- Alternatively, run Neo4j from the browser at [http://localhost:7474](http://localhost:7474)

---

## 🧪 Environment Setup

### Create a `.env` file in the **project root**:

   ```env
   NEO4J_URI=bolt://localhost:7687       # Default connection URI
   NEO4J_USER=neo4j                      # Default user (change if needed)
   NEO4J_PASSWORD=your_password          # Replace with your actual password
   ```

## 📁 Code Structure
```commandline
project_root/
├── app/
│   ├── __init__.py
│   ├── config.py        # Loads environment
│   ├── db.py            # Handles Neo4j connection
│   ├── commands.py      # Transaction functions (e.g. add_person)
│   └── main.py          # Entrypoint
│
├── tests/
│   ├── __init__.py
│   └── test_commands.py # Tests using pytest
│
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── poetry.lock
├── pyproject.toml
└── README.md
```

## 🚀 Quickstart

### 📦 Install Dependencies (with Poetry 2.0.1)

Make sure you have Python ≥ 3.13 installed:

```bash
python --version
# Python 3.13.0
```

Install Poetry and set up the environment:
```commandline
python -m pip install poetry==2.0.1
poetry env use python
poetry install --no-root
```

### ▶️ Run the Application
Open Neo4j Desktop and start the database
Start backend server (from root folder)
```commandline
poetry run uvicorn app.main:app --reload
```
Start frontend server (from root folder)
```commandline
cd frontend
npm run dev
```


### ✅ Testing
#### 🛠️ Setup Test Environment
Add the following to your **.env** file for test database access:
```env
NEO4J_FOR_TESTS_URI=bolt://localhost:7687       # Default test URI
NEO4J_FOR_TESTS_USER=neo4j                      # Test user
NEO4J_FOR_TESTS_PASSWORD=your_password          # Test password
```

#### 🧪 Run Tests
```commandline
poetry run pytest
```

### Common Errors
#### 1.
Sometimes fastapi server doesn't respond properly especially after multiple restarts. Check whether the port is free (ex. checking port 8000):
```commandline
netstat -ano | findstr :8000
```
Try to kill conflicting PID (ex. 2916):
```commandline
taskkill /PID 2916 /F
```
If that doesn't work use different port (ex. 8010):
```commandline
poetry run uvicorn app.main:app --reload --port 8010
```
