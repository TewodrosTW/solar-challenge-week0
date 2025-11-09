# solar-challenge-week0
This repo has been created for learning and training purpose.

## Environment Setup

This section explains how to reproduce the development environment from scratch.

### Prerequisites

Before starting, ensure you have the following installed:
- **Python 3.10 or higher** - Check your version with `python3 --version`
- **pip** - Usually comes with Python, verify with `pip --version`
- **Git** - For cloning the repository

### Steps to Reproduce the Environment

#### 1. Clone the Repository

If you haven't already cloned the repository:

```bash
git clone git@github.com:TewodrosTW/solar-challenge-week0.git
cd solar-challenge-week0
```

#### 2. Create a Virtual Environment

Create an isolated Python environment to avoid conflicts with system packages:

```bash
python3 -m venv venv
```

This creates a `venv` directory containing the virtual environment.

#### 3. Activate the Virtual Environment

Activate the virtual environment before installing packages or running scripts:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

You should see `(venv)` at the beginning of your terminal prompt when activated.

#### 4. Upgrade pip (Recommended)

Ensure you have the latest version of pip:

```bash
pip install --upgrade pip
```

#### 5. Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### 6. Verify the Installation

Confirm everything is set up correctly:

```bash
python --version
pip list
```

### Deactivating the Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```

### Troubleshooting

- **If `python3` command not found**: Try `python` instead, or ensure Python 3 is installed
- **If activation fails on Windows**: You may need to run PowerShell as Administrator or change execution policy
- **If packages fail to install**: Make sure the virtual environment is activated and pip is up to date

### Notes

- The `venv/` directory is in `.gitignore` and won't be committed to the repository
- Always activate the virtual environment before working on the project
- To update `requirements.txt` after adding new packages:
  ```bash
  pip freeze > requirements.txt
  ```
