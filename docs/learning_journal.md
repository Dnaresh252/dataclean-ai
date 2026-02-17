# 📚 Learning Journal - DataClean.AI

## Week 1: Setup & Foundations

### What I Learned

**Day 1: Tool Installation**

- Installed Python, VS Code, Node.js, Git, Docker
- Why: These are industry-standard tools for full-stack + ML development
- Challenge: Docker required WSL2 on Windows (solved by enabling it)

**Day 2: Project Structure**

- Created organized folder structure
- Why: Professional projects need clear organization
- Learning: Separation of concerns (ML code separate from API code)

**Day 3: Python Environment**

- Created virtual environment
- Installed packages (FastAPI, scikit-learn, etc.)
- Why: Isolates dependencies, prevents conflicts
- Learning: requirements.txt tracks exact versions

**Day 4: Backend Basics**

- Created basic FastAPI app
- Why: FastAPI is modern, fast, has automatic docs
- Learning: Async programming basics, CORS, middleware

**Day 5: Jupyter Setup**

- Setup Jupyter Lab for ML experiments
- Why: Interactive coding for data science
- Learning: Difference between notebooks (experiments) vs scripts (production)

### Questions I Had

Q: Why FastAPI instead of Flask?
A: FastAPI is newer, faster, has automatic validation and docs, async support

Q: Why Docker for database?
A: Keeps system clean, easy to reset, same environment as production

Q: Why separate notebooks and ml_pipeline folders?
A: Notebooks = experiments/exploration, ml_pipeline = production code

### Next Steps

- Week 2: Start collecting training data
- Build data labeling tool
- Begin exploratory data analysis

### Resources Used

- FastAPI docs: https://fastapi.tiangolo.com
- Docker docs: https://docs.docker.com
- Python venv guide: https://docs.python.org/3/tutorial/venv.html
