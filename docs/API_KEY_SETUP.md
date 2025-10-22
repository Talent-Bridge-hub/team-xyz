# 🔑 How to Get Your API Keys (Step-by-Step)

## Option 1: SerpAPI (RECOMMENDED) ⭐

### Step 1: Sign Up
1. Go to: https://serpapi.com/users/sign_up
2. Enter your email and create password
3. Click "Sign Up" (NO credit card needed!)

### Step 2: Get API Key
1. After signup, you'll see your dashboard
2. Look for "API Key" section (top of page)
3. Copy the key (looks like: `abc123def456ghi789...`)

### Step 3: Give Me the Key
Paste it here or add to `.env` file:
```bash
SERPAPI_KEY=your_key_here
```

### Step 4: Test It
I'll test it with this command:
```python
from serpapi import GoogleSearch

params = {
    "engine": "google_jobs",
    "q": "software engineer Tunisia",
    "api_key": "YOUR_KEY"
}
search = GoogleSearch(params)
results = search.get_dict()
print(f"Found {len(results['jobs_results'])} jobs!")
```

**What you'll get:** 100 free searches/month

---

## Option 2: RapidAPI JSearch

### Step 1: Sign Up for RapidAPI
1. Go to: https://rapidapi.com/auth/sign-up
2. Sign up with email or Google account
3. Verify your email

### Step 2: Subscribe to JSearch API
1. Go to: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
2. Click "Subscribe to Test" button
3. Select "Basic" plan (FREE - 250 requests/month)
4. Click "Subscribe"

### Step 3: Get API Key
1. After subscribing, you'll see "X-RapidAPI-Key" in the code snippets
2. Copy the key (looks like: `abc123xyz...`)
3. Also note the "X-RapidAPI-Host": `jsearch.p.rapidapi.com`

### Step 4: Give Me Both Values
```bash
RAPIDAPI_KEY=your_key_here
RAPIDAPI_HOST=jsearch.p.rapidapi.com
```

**What you'll get:** 250 free requests/month

---

## Option 3: Adzuna API

### Step 1: Sign Up
1. Go to: https://developer.adzuna.com/signup
2. Fill in the form (name, email, company name)
3. Agree to terms and submit

### Step 2: Get Credentials
1. Check your email for API credentials
2. You'll receive TWO values:
   - Application ID (looks like: `12345678`)
   - Application Key (looks like: `abc123def456...`)

### Step 3: Give Me Both
```bash
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

**What you'll get:** Unlimited free requests (with attribution)

---

## Option 4: No API Key Needed (Custom Scraping)

If you choose custom scraping, I'll implement it without any API key. Just tell me:
- Which sites to scrape? (Bayt.com, Tanqeeb.com, LinkedIn, Indeed)
- Which regions? (Tunisia, Egypt, Morocco, Nigeria, etc.)

---

## 🎯 My Recommendation

**START HERE:**

1. **Get SerpAPI key** (5 minutes, easiest)
   - Best reliability
   - Clean data
   - 100 free searches is enough for testing

2. **Later, add RapidAPI** (if you need more)
   - 250 free requests
   - Good backup

3. **Then add custom scraping** (for MENA sites)
   - Bayt.com integration
   - Tanqeeb.com integration

This gives you **350+ free job searches per month** across all major job boards!

---

## 📝 Once You Have the Key

Just tell me:
```
"I have a SerpAPI key: [YOUR_KEY]"
```

Or paste it directly into `.env` file:
```bash
nano .env
# Add this line:
SERPAPI_KEY=your_actual_key_here
```

Then I'll:
1. ✅ Install the API library
2. ✅ Create job scraper module
3. ✅ Test with your key
4. ✅ Show you REAL jobs from Tunisia, Egypt, Morocco, etc.
5. ✅ Integrate with job matcher

**Ready in 1 hour!** 🚀

---

## ⚡ Quick Start (Copy-Paste Ready)

Once you have your key, just run:

```bash
# Add key to .env file
echo "SERPAPI_KEY=your_key_here" >> .env

# I'll then run:
source venv/bin/activate
pip install google-search-results
python utils/job_scraper.py --test
```

---

## 🆘 Need Help?

If you have trouble getting the API key:
1. Take a screenshot of where you're stuck
2. Share it with me
3. I'll guide you through it step-by-step

**Let's get those real jobs scraped!** 🎯
