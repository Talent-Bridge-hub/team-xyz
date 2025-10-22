# UtopiaHire: AI Career Architect

An AI-powered platform promoting fairness and inclusivity in employment across Sub-Saharan Africa and MENA regions.

## 🎯 Current Progress: 100% Complete! 🎉

**✅ Module 1: Resume Reviewer** - COMPLETE  
**✅ Module 2: Job Matcher with REAL Jobs** - COMPLETE ⭐ Real apply URLs!  
**✅ Module 3: AI Interviewer** - COMPLETE ⭐ Practice interviews with AI feedback!  
**✅ Module 4: Footprint Scanner** - COMPLETE ⭐ NEW: GitHub + Stack Overflow analysis!

## 📁 Project Structure

```
Utopia/
├── venv/                  # Python virtual environment (isolated packages)
├── backend/               # Backend logic and API endpoints
├── models/                # AI models and training scripts
├── utils/                 # Utility functions (parsing, formatting, etc.)
├── config/                # Configuration files (database, API keys, etc.)
├── cli/                   # Command-line interface scripts
├── data/
│   ├── resumes/          # Input resumes (PDF/DOCX)
│   └── outputs/          # Analysis results and improved resumes
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Technology Stack

- **Language**: Python 3.12
- **Database**: PostgreSQL 16
- **AI/ML**: Ollama (Local LLM), Transformers, SpaCy
- **PDF Processing**: PyPDF2, PDFPlumber, python-docx
- **CLI**: Click + Rich (beautiful terminal UI)

## 🚀 Setup Instructions

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Create database
sudo -u postgres psql -c "CREATE DATABASE utopiahire;"
sudo -u postgres psql -c "CREATE USER utopia_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE utopiahire TO utopia_user;"
```

### 4. Install Ollama (Local AI)
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

## 💡 How It Works

### Module 1: Resume Reviewer
1. **Upload**: User uploads PDF/DOCX resume
2. **Parse**: Extract text, identify sections (education, skills, experience)
3. **Analyze**: 
   - Check ATS compatibility
   - Evaluate formatting
   - Identify missing keywords
   - Score against industry standards
4. **Enhance**: AI suggests improvements using fine-tuned prompts
5. **Export**: Generate improved resume + detailed report

### Module 2: Job Matcher with REAL Jobs ⭐
1. **Scrape Real Jobs**: Fetch from SerpAPI, LinkedIn, Indeed (100+ jobs)
2. **Parse Resume**: Extract candidate skills, experience level, location
3. **Match Jobs**: AI-powered matching with 119+ real opportunities
4. **Score Matches**: Multi-dimensional scoring (skills 60%, location 20%, experience 20%)
5. **Apply URLs**: Every job includes direct apply link for frontend
6. **Market Insights**: Real-time salary ranges, demand trends, top skills

### Module 3: AI Interviewer ⭐
1. **Practice Interviews**: Simulate real job interviews in a safe environment
2. **Smart Questions**: 14+ curated questions (technical, behavioral, situational)
3. **AI Analysis**: 5-dimensional scoring (relevance, completeness, clarity, technical, communication)
4. **Instant Feedback**: Strengths, weaknesses, missing points, suggestions
5. **Progress Tracking**: Track improvement across sessions
6. **MENA/Africa Focus**: Region-specific questions and scenarios

### Module 4: Footprint Scanner ⭐ NEW
1. **GitHub Analysis**: Repos, stars, forks, contribution activity, code quality
2. **Stack Overflow Analysis**: Reputation, badges, answers, expertise areas
3. **Comprehensive Scoring**: 4-dimensional (Visibility, Activity, Impact, Expertise)
4. **Trend Tracking**: Monitor progress over time
5. **Actionable Insights**: Personalized recommendations to improve
6. **Performance Levels**: Excellent (85+), Good (70-84), Average (55-69), Needs Improvement (0-54)

**All Commands:**
- `./utopiahire analyze resume.pdf` - Analyze resume
- `./utopiahire enhance resume.pdf` - Get improvement suggestions
- `./utopiahire interview` - Start AI interview practice
- `./utopiahire history` - View past interview sessions
- `./utopiahire scrape` - Fetch fresh real jobs from APIs
- `./utopiahire match resume.pdf` - Find matches with apply URLs
- `./utopiahire market --region MENA` - Get market insights
- `./utopiahire scan --github USERNAME --stackoverflow ID` - Scan professional footprint
- `./utopiahire footprint` - View footprint score
- `./utopiahire trends` - Track score trends over time

## 🎓 For Beginners: Key Concepts

- **Virtual Environment**: Isolated Python packages (won't mess up system Python)
- **PostgreSQL**: Database to store user data, resumes, analysis results
- **Ollama**: Runs AI models locally (no internet needed, privacy-first)
- **CLI**: Command-line interface - interact via terminal before building web UI
- **Fine-tuning**: Customizing AI models for specific resume tasks

## 📊 Database Schema

```sql
-- Users table
users (id, name, email, region, created_at)

-- Resumes table
resumes (id, user_id, filename, raw_text, parsed_data, uploaded_at)

-- Analysis results
analyses (id, resume_id, ats_score, formatting_score, suggestions, created_at)

-- Improved resumes
improved_resumes (id, resume_id, enhanced_text, changes_made, created_at)
```

## 🔐 Privacy & Security

- All processing happens locally (no external API calls)
- Resume data stored securely in PostgreSQL
- No data sharing with third parties
- User controls their own data

## 📈 Next Steps

- [ ] Setup database
- [ ] Install AI models
- [ ] Build resume parser
- [ ] Create analyzer module
- [ ] Implement CLI
- [ ] Test with sample resumes

---

**Built for IEEE TSYP13 Technical Challenge**
