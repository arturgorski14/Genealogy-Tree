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

TODO: diagrams about cqrs

Domain → pure business logic (Person aggregate).
Application → orchestrates actions (commands/queries/handlers).
Infrastructure → persistence & integration (repositories, external systems)

## 🚀 Quickstart

### 📦 Install Dependencies (with uv 0.8.15)

Make sure you have Python ≥ 3.13 installed:

```bash
python --version
# Python 3.13.0
```

Set up the virtual environment and install dependencies:
```commandline
uv venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/macOS
uv sync
```

### ▶️ Run the Application
Open Neo4j Desktop and start the database
Start backend server (from root folder)
```commandline
uv run uvicorn app.main:app --reload
```
Start frontend server (from root folder)
```commandline
cd frontend
npm run dev
```


### ✅ Testing
#### 🛠️ Setup Test Environment

#### 🧪 Run Tests
```commandline
uv run pytest
```

### Contributing
#### Usefull commands
Clean the files without needing to commit
```commandline
pre-commit run --all-files
```
Generate coverage report
```commandline
uv run pytest --cov=app --cov-report=term-missing
```
Remove local branches (fully merged to main)
- Windows
```commandline
git branch | Where-Object { $_ -notmatch "main" } | ForEach-Object { git branch -d $_.Trim() }
```
- Linux
```commandline
git branch | grep -v "main" | xargs git branch -d
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
uv run uvicorn app.main:app --reload --port 8010
```
