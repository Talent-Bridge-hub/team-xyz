# 🔍 Real Job Scraping API Research & Implementation Plan

**Goal:** Replace sample job database with REAL job opportunities from LinkedIn, Indeed, Bayt.com, etc.

---

## 📊 API Comparison: Free Tier Options

### 1. **SerpAPI** ⭐⭐⭐⭐⭐ (RECOMMENDED)
**Website:** https://serpapi.com/  
**Free Tier:** 100 searches/month  
**Best For:** Google Jobs, Indeed, LinkedIn scraping

**Pros:**
- ✅ Official Google Jobs API integration
- ✅ Clean JSON responses
- ✅ Supports multiple job boards (Indeed, LinkedIn, Glassdoor)
- ✅ Location filtering (by city, country)
- ✅ Salary data included
- ✅ No proxy/CAPTCHA issues
- ✅ Well-documented Python library

**Cons:**
- ❌ Limited to 100 searches/month on free tier
- ❌ $50/month for 5,000 searches (paid tier)

**Sample Response:**
```json
{
  "jobs_results": [
    {
      "title": "Software Engineer",
      "company_name": "TechCorp",
      "location": "Tunis, Tunisia",
      "description": "Develop web applications...",
      "detected_extensions": {
        "posted_at": "2 days ago",
        "schedule_type": "Full-time"
      },
      "salary": "€2,500 - €4,000/month"
    }
  ]
}
```

**API Endpoint:**
```python
import requests

params = {
    "engine": "google_jobs",
    "q": "software engineer",
    "location": "Tunis, Tunisia",
    "api_key": "YOUR_API_KEY"
}
response = requests.get("https://serpapi.com/search", params=params)
```

---

### 2. **RapidAPI - JSearch** ⭐⭐⭐⭐
**Website:** https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch  
**Free Tier:** 250 requests/month  
**Best For:** Indeed, LinkedIn, Glassdoor

**Pros:**
- ✅ Higher free tier (250 requests)
- ✅ Multiple job boards support
- ✅ Salary estimation
- ✅ Experience level filtering
- ✅ Remote job filtering

**Cons:**
- ❌ Requires RapidAPI account
- ❌ Response format varies by job board

**Sample API Call:**
```python
import requests

url = "https://jsearch.p.rapidapi.com/search"
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}
params = {
    "query": "Python developer in Tunisia",
    "page": "1",
    "num_pages": "1"
}
response = requests.get(url, headers=headers, params=params)
```

---

### 3. **Adzuna API** ⭐⭐⭐⭐
**Website:** https://developer.adzuna.com/  
**Free Tier:** Unlimited (with attribution)  
**Best For:** Multiple countries including some African markets

**Pros:**
- ✅ **Truly free** with no hard limits
- ✅ Covers 19 countries
- ✅ Salary data included
- ✅ Category/tag filtering
- ✅ Distance-based search

**Cons:**
- ❌ Limited coverage in MENA/Africa (mainly UK, US, EU)
- ❌ Requires displaying "Powered by Adzuna" attribution
- ❌ Less data for Tunisia, Morocco, Egypt

**Sample API Call:**
```python
import requests

app_id = "YOUR_APP_ID"
app_key = "YOUR_APP_KEY"

url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
params = {
    "app_id": app_id,
    "app_key": app_key,
    "results_per_page": 20,
    "what": "python developer",
    "where": "london"
}
response = requests.get(url, params=params)
```

---

### 4. **Custom Scraping (BeautifulSoup + Requests)** ⭐⭐⭐
**Free Tier:** Unlimited (self-hosted)  
**Best For:** Direct scraping of job boards

**Target Sites:**
- **Bayt.com** - MENA's largest job site
- **Tanqeeb.com** - MENA focused
- **LinkedIn Jobs** (public pages)
- **Indeed.com**

**Pros:**
- ✅ Completely free
- ✅ Full control over data extraction
- ✅ Can target regional job boards (Bayt, Tanqeeb)
- ✅ No API rate limits

**Cons:**
- ❌ Requires maintenance (sites change HTML structure)
- ❌ Risk of IP blocking
- ❌ CAPTCHA challenges
- ❌ Legal gray area (check ToS)
- ❌ More complex implementation

**Sample Scraper:**
```python
import requests
from bs4 import BeautifulSoup

def scrape_bayt():
    url = "https://www.bayt.com/en/tunisia/jobs/software-engineer/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    for job_card in soup.find_all('li', class_='has-pointer-d'):
        title = job_card.find('h2').text.strip()
        company = job_card.find('b', class_='t-default').text.strip()
        # ... extract more fields
        jobs.append({'title': title, 'company': company})
    
    return jobs
```

---

## 🎯 RECOMMENDATION: Hybrid Approach

**Best Strategy for UtopiaHire:**

### Phase 1: Start with SerpAPI (Google Jobs)
- **Why:** Most reliable, covers multiple job boards, clean data
- **Cost:** Free tier (100 searches/month) is enough for demo/testing
- **Implementation:** 2-3 hours

### Phase 2: Add Custom Scraping for Regional Boards
- **Target:** Bayt.com, Tanqeeb.com (MENA specific)
- **Why:** These boards have better MENA/Africa coverage
- **Implementation:** 1-2 days

### Phase 3 (Optional): Add RapidAPI JSearch as backup
- **Why:** Higher rate limit, fallback if SerpAPI quota exhausted
- **Cost:** Free tier (250 requests/month)

---

## 📋 WHAT I NEED FROM YOU

To implement real job scraping, please provide:

### 1. **API Key (Choose One):**

#### Option A: SerpAPI (Recommended)
1. Go to: https://serpapi.com/users/sign_up
2. Create free account (no credit card needed)
3. Get your API key from dashboard
4. **Give me:** Your SerpAPI key

#### Option B: RapidAPI JSearch
1. Go to: https://rapidapi.com/auth/sign-up
2. Subscribe to JSearch API (free tier)
3. Copy API key from dashboard
4. **Give me:** Your RapidAPI key

#### Option C: Adzuna
1. Go to: https://developer.adzuna.com/signup
2. Create account and get API credentials
3. **Give me:** App ID + App Key

### 2. **Target Regions & Keywords:**
Tell me:
- Which regions to prioritize? (Tunisia, Egypt, Morocco, Nigeria, Kenya, etc.)
- Which job titles to search? (Software Engineer, Data Analyst, etc.)
- Preferred job boards? (LinkedIn, Indeed, Bayt, Tanqeeb, etc.)

### 3. **Scraping Frequency:**
- How often to update jobs? (Daily, Weekly, On-demand)
- How many jobs to fetch per search?

---

## 🚀 IMPLEMENTATION PLAN (Once You Provide API Key)

### Step 1: Install Dependencies (5 minutes)
```bash
pip install serpapi requests beautifulsoup4
```

### Step 2: Create Job Scraper Module (1 hour)
```python
# utils/job_scraper.py
- scrape_google_jobs(query, location, api_key)
- scrape_bayt_jobs(query, location)  # Custom scraper
- normalize_job_data()  # Standardize format
- save_to_database()
```

### Step 3: Update Database Schema (30 minutes)
```sql
-- Add new table: scraped_jobs
CREATE TABLE scraped_jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(255),
    description TEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    currency VARCHAR(10),
    url TEXT,
    source VARCHAR(50),  -- 'google_jobs', 'bayt', etc.
    scraped_at TIMESTAMP,
    expires_at TIMESTAMP
);
```

### Step 4: Update Job Matcher (1 hour)
```python
# Replace SAMPLE_JOBS with real database queries
jobs_database = get_scraped_jobs_from_db(region='MENA')
```

### Step 5: Add CLI Command (30 minutes)
```bash
# New command to refresh job database
./utopiahire scrape --region MENA --keywords "software engineer"
```

### Step 6: Testing (1 hour)
- Test API integration
- Verify data quality
- Check match scoring with real jobs

**Total Implementation Time:** 4-5 hours (with API key)

---

## 💡 IMMEDIATE NEXT STEPS

### For You:
1. **Choose API provider** (I recommend SerpAPI)
2. **Sign up and get API key** (takes 2 minutes)
3. **Share API key with me** (paste here or in .env file)
4. **Tell me target regions** (which countries to focus on)

### For Me:
Once you provide the above, I will:
1. ✅ Install API client library
2. ✅ Create `utils/job_scraper.py`
3. ✅ Update database schema
4. ✅ Integrate with job matcher
5. ✅ Add CLI command for scraping
6. ✅ Test with real job data

---

## 📊 EXPECTED OUTCOME

After implementation:
```bash
# Scrape real jobs
./utopiahire scrape --region Tunisia --keywords "Python developer"

# Match with real jobs
./utopiahire match resume.pdf
# Output:
# ✓ Found 15 REAL job matches from LinkedIn, Indeed, Bayt
# 1. Software Engineer at TechStart (Tunis) - 87% match
# 2. Python Developer at InnovateLab (Casablanca) - 82% match
# ... (13 more real jobs)
```

---

## ⚠️ ALTERNATIVE: Start with Custom Scraping (No API Key Needed)

If you don't want to use paid APIs, I can implement **custom scraping** for Bayt.com and Tanqeeb.com right now (no API key needed). This will take longer (1-2 days) and be less reliable, but it's completely free.

**Let me know your preference!**

---

**What would you like to do?**
1. Get SerpAPI key and I'll integrate it (recommended - fastest)
2. Get RapidAPI key and I'll integrate JSearch
3. Skip APIs and do custom scraping (slower but free)
4. Do hybrid approach (API + custom scraping)
