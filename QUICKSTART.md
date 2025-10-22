# 🚀 Quick Start Guide - UtopiaHire

## Daily Workflow

### 1. Start Working
```bash
cd /home/firas/Utopia
source venv/bin/activate  # Activate Python environment
```

### 2. Start PostgreSQL (if not running)
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### 3. Test Everything is Working
```bash
# Test database
python config/database.py

# Test resume parser
python -c "from utils.resume_parser import ResumeParser; print('✓ Parser ready!')"
```

---

## Useful Commands

### Python Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate when done
deactivate

# Install new package
pip install package_name

# List installed packages
pip list
```

### Database
```bash
# Connect to database
PGPASSWORD=utopia_secure_2025 psql -h localhost -U utopia_user -d utopiahire

# Once connected, you can:
\dt                          # List all tables
\d table_name                # Describe table structure
SELECT * FROM users;         # Query data
\q                           # Quit
```

### File Structure
```bash
# Navigate
cd /home/firas/Utopia

# List files
ls -la

# View file
cat filename.py

# Edit file  
nano filename.py  # or use VS Code
```

---

## Common Tasks

### Parse a New Resume
```python
from utils.resume_parser import ResumeParser

parser = ResumeParser()
result = parser.parse_file('/path/to/resume.pdf')
print(result['structured_data']['skills'])
```

### Query Database
```python
from config.database import execute_query

# Get all users
users = execute_query("SELECT * FROM users")
print(users)

# Insert a user
from config.database import insert_one
user_id = insert_one('users', {
    'name': 'Test User',
    'email': 'test@example.com',
    'region': 'Tunisia'
})
```

### Create Sample Resume
```bash
python utils/create_sample_resume.py
```

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Install missing package
pip install package_name
```

### "Database connection failed"
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start if not running
sudo systemctl start postgresql
```

### "Permission denied"
```bash
# Fix file permissions
chmod +x filename.sh
# or
chmod 644 filename.py
```

### Import Errors
```bash
# Make sure you're in the right directory
cd /home/firas/Utopia

# Add current directory to Python path
export PYTHONPATH=/home/firas/Utopia:$PYTHONPATH
```

---

## Project Files Explained

### Core Files
- **`.env`** - Configuration (passwords, settings)
- **`requirements.txt`** - Python dependencies
- **`README.md`** - Project documentation
- **`PROGRESS.md`** - What we've accomplished

### Code Modules
- **`config/database.py`** - Database operations
- **`config/schema.sql`** - Database structure
- **`utils/resume_parser.py`** - Resume parsing logic
- **`utils/create_sample_resume.py`** - Test data generator

### Data Folders
- **`data/resumes/`** - Input resume files
- **`data/outputs/`** - Analysis results
- **`venv/`** - Python packages (don't modify)

---

## Next Session Checklist

Before starting next time:
- [ ] `cd /home/firas/Utopia`
- [ ] `source venv/bin/activate`
- [ ] `sudo systemctl start postgresql`
- [ ] `python config/database.py` (test)
- [ ] Ready to code!

---

## Getting Help

### Python Errors
1. Read the error message carefully
2. Check if module is installed: `pip list | grep module_name`
3. Check if virtual environment is active: `which python`

### Database Errors
1. Check PostgreSQL is running: `sudo systemctl status postgresql`
2. Test connection: `python config/database.py`
3. Check credentials in `.env` file

### General Issues
1. Check you're in the right directory
2. Check file permissions
3. Check virtual environment is activated

---

## Performance Tips

### Your VM Specs: 6 cores, 8GB RAM, 40GB storage
- ✅ Perfect for this project
- ✅ Can handle multiple AI models
- ✅ Database will be fast
- ⚠️ Don't run too many programs simultaneously
- ⚠️ Monitor disk space: `df -h`

### Speed Things Up
```bash
# Check RAM usage
free -h

# Check disk space
df -h

# Check running processes
top
# (Press 'q' to quit)
```

---

## Backup Your Work

### Important Files to Backup
```bash
# Create backup
tar -czf utopiahire_backup.tar.gz \
  .env \
  config/ \
  utils/ \
  backend/ \
  models/ \
  cli/ \
  README.md \
  requirements.txt

# Restore from backup
tar -xzf utopiahire_backup.tar.gz
```

### Git (for IEEE submission)
```bash
# Initialize git (when ready)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub (create repo first on github.com)
git remote add origin https://github.com/yourusername/utopiahire.git
git push -u origin main
```

---

## Key Concepts (Remember These!)

### Virtual Environment
- Isolated Python packages
- Activate: `source venv/bin/activate`
- Deactivate: `deactivate`

### PostgreSQL
- Database service: Must be running
- Database name: `utopiahire`
- Username: `utopia_user`
- Password: in `.env` file

### Resume Parser
- Takes PDF/DOCX → Returns structured data
- Automatically detects sections
- Extracts contact info, skills, education

### ATS (Applicant Tracking System)
- Software companies use to filter resumes
- We optimize resumes to pass ATS filters
- Checks keywords, formatting, readability

---

Made with 💚 for Beginners
Last Updated: October 14, 2025
