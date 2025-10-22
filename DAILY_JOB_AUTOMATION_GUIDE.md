# 🤖 Daily Job Update Automation Guide

## Overview

The **Daily Job Updater** automatically updates job opportunities every day while **carefully managing API limits** to ensure you never run out before the month ends.

---

## 🎯 Key Features

### 1. **Smart API Usage Management**
- Tracks API usage across the month
- Calculates daily budget based on remaining days
- Reserves 10% buffer for emergencies
- Auto-resets counters each new month

### 2. **Intelligent Search Strategy**
Different job types/regions each day of the week:
- **Monday**: MENA Tech Jobs (Software, Frontend, Backend)
- **Tuesday**: Sub-Saharan Africa Tech Jobs
- **Wednesday**: Data & Analytics Jobs
- **Thursday**: DevOps & Cloud Jobs
- **Friday**: Design & Product Jobs
- **Saturday**: Remote Opportunities
- **Sunday**: Popular Roles (Mixed Regions)

### 3. **Automatic Maintenance**
- Removes jobs older than 30 days
- Prevents database bloat
- Keeps jobs fresh and relevant

### 4. **Comprehensive Logging**
- All operations logged to `/home/firas/Utopia/logs/job_updater.log`
- API usage tracked in `/home/firas/Utopia/logs/api_usage.json`
- Easy monitoring and troubleshooting

---

## 📊 API Budget Management

### Monthly Limits
```
SerpAPI:           100 searches/month
LinkedIn RapidAPI: 500 requests/month
JSearch RapidAPI:  250 requests/month
```

### How Daily Budget is Calculated

```python
# Example: Today is October 16th
Days in October = 31
Days remaining = 31 - 16 + 1 = 16 days

SerpAPI used so far = 20
SerpAPI remaining = 100 - 20 = 80
Safe remaining (90%) = 80 * 0.9 = 72

Daily budget = 72 / 16 = 4.5 ≈ 4 searches/day
```

This ensures you **never run out** before the month ends!

---

## 🚀 Quick Start

### Option 1: Run Once Manually

```bash
# Run the daily update now
python daily_job_updater.py

# Takes ~5 minutes
# Adds 30-50 new jobs per run
```

### Option 2: Setup Daily Automation (Recommended)

```bash
# Show cron setup instructions
python daily_job_updater.py --setup-cron

# Then follow the instructions to add to crontab
```

**Manual Setup:**
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2:00 AM):
0 2 * * * cd /home/firas/Utopia && /usr/bin/python3 /home/firas/Utopia/daily_job_updater.py >> /home/firas/Utopia/logs/cron.log 2>&1
```

### Option 3: Check API Usage

```bash
# View current API usage statistics
python daily_job_updater.py --check-usage
```

Output example:
```
📊 API USAGE STATISTICS
=====================================
Month: 2025-10

📈 Usage by API:

  serpapi:
    Used: 20/100 (20.0%)
    Remaining: 80
    [████████░░░░░░░░░░░░░░░░░░░░]

  linkedin_rapidapi:
    Used: 0/500 (0.0%)
    Remaining: 500
    [░░░░░░░░░░░░░░░░░░░░░░░░░░░░]

📅 Days remaining this month: 16

💰 Daily Budget:
  serpapi: 4 calls/day
  linkedin_rapidapi: 28 calls/day
```

---

## 📝 Daily Update Flow

### What Happens Each Day

1. **Calculate Budget**
   - Load usage stats from file
   - Check if new month (reset if needed)
   - Calculate safe daily budget

2. **Get Today's Strategy**
   - Based on day of week
   - 3-4 targeted searches
   - Different regions/roles each day

3. **Scrape Jobs**
   - Use multi-API system with fallback
   - Respect daily budget limits
   - 3-second delay between searches

4. **Store in Database**
   - Check for duplicates (skip if exists)
   - Auto-determine region (MENA, Sub-Saharan Africa, Other)
   - Store with all job details

5. **Cleanup Old Jobs**
   - Remove jobs older than 30 days
   - Keep database fresh

6. **Update Usage Stats**
   - Track API calls made
   - Save to file for next run
   - Log summary

### Expected Results Per Run

```
Jobs scraped:     30-50 jobs
New jobs stored:  20-40 jobs (some duplicates skipped)
API calls made:   3-4 calls
Time taken:       3-5 minutes
Old jobs removed: 5-15 jobs (depends on age)
```

---

## 📈 Weekly Coverage Example

| Day       | Focus                         | Searches | New Jobs |
|-----------|-------------------------------|----------|----------|
| Monday    | MENA Tech                     | 3        | ~30      |
| Tuesday   | Sub-Saharan Africa Tech       | 3        | ~30      |
| Wednesday | Data & Analytics              | 3        | ~30      |
| Thursday  | DevOps & Cloud                | 3        | ~30      |
| Friday    | Design & Product              | 3        | ~30      |
| Saturday  | Remote Opportunities          | 2        | ~30      |
| Sunday    | Popular Roles (Mixed)         | 3        | ~30      |
| **Total** |                               | **20**   | **~210** |

### Monthly Projection
- **Searches per month**: ~20/week × 4 weeks = **80 searches**
- **Buffer remaining**: 100 - 80 = **20 searches** (emergency reserve)
- **New jobs per month**: ~210/week × 4 = **~840 jobs**
- **Jobs in database**: ~300-400 (after cleanup)

---

## 🔍 Monitoring & Maintenance

### Check Logs

```bash
# View recent activity
tail -50 /home/firas/Utopia/logs/job_updater.log

# Watch live updates
tail -f /home/firas/Utopia/logs/job_updater.log

# Check cron execution
tail -50 /home/firas/Utopia/logs/cron.log
```

### Check Database Stats

```bash
# Connect to database
psql -U postgres -d utopia_db

# Run queries
SELECT COUNT(*) as total FROM jobs;

SELECT region, COUNT(*) as count 
FROM jobs 
GROUP BY region 
ORDER BY count DESC;

SELECT COUNT(*) as recent_jobs 
FROM jobs 
WHERE posted_date >= CURRENT_DATE - INTERVAL '7 days';
```

### API Usage Monitoring

```bash
# Check usage anytime
python daily_job_updater.py --check-usage

# View usage file directly
cat /home/firas/Utopia/logs/api_usage.json
```

Example `api_usage.json`:
```json
{
  "month": "2025-10",
  "serpapi": 24,
  "linkedin_rapidapi": 0,
  "jsearch_rapidapi": 0,
  "last_updated": "2025-10-16T14:32:18.123456"
}
```

---

## ⚙️ Customization

### Change Daily Schedule

Edit the cron time in `crontab -e`:

```bash
# Run at 6:00 AM instead of 2:00 AM
0 6 * * * cd /home/firas/Utopia && /usr/bin/python3 /home/firas/Utopia/daily_job_updater.py >> /home/firas/Utopia/logs/cron.log 2>&1

# Run twice a day (2 AM and 2 PM)
0 2,14 * * * cd /home/firas/Utopia && /usr/bin/python3 /home/firas/Utopia/daily_job_updater.py >> /home/firas/Utopia/logs/cron.log 2>&1
```

### Modify Search Strategies

Edit `daily_job_updater.py` method `get_todays_search_strategy()`:

```python
0: {  # Monday
    'name': 'Your Custom Strategy',
    'searches': [
        {'query': 'Your Job Title', 'location': 'Your City', 'count': 10},
        {'query': 'Another Title', 'location': 'Another City', 'count': 15},
    ]
},
```

### Adjust Job Retention Period

Edit `cleanup_old_jobs()` method:

```python
# Change from 30 days to 45 days
cutoff_date = (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d')
```

### Modify API Safety Buffer

Edit `calculate_daily_budget()` method:

```python
# Change from 10% to 20% reserve
safe_remaining = int(remaining * 0.8)  # Was 0.9
```

---

## 🐛 Troubleshooting

### Problem: Cron job not running

**Check if cron service is running:**
```bash
sudo systemctl status cron
```

**Check crontab is configured:**
```bash
crontab -l
```

**Check cron logs:**
```bash
tail -50 /home/firas/Utopia/logs/cron.log
```

**Solution:**
```bash
# Start cron service
sudo systemctl start cron

# Enable on boot
sudo systemctl enable cron
```

### Problem: No new jobs being added

**Check API usage:**
```bash
python daily_job_updater.py --check-usage
```

**If APIs are exhausted:**
- Wait until next month (auto-resets)
- Or use fallback manual scraping

**Check logs for errors:**
```bash
tail -100 /home/firas/Utopia/logs/job_updater.log | grep ERROR
```

### Problem: Too many duplicates

**This is normal!** The system checks for duplicates by `job_id`.

If a job exists, it's skipped. This means:
- ✅ No duplicate jobs in database
- ✅ API calls are still useful (verifying job is still active)

**To reduce duplicates:**
- Modify search strategies to focus on different regions
- Increase variety of job titles searched

### Problem: API rate limit hit

**Daily budget exceeded:**
- System will limit searches automatically
- Check usage: `python daily_job_updater.py --check-usage`
- Wait until tomorrow for budget reset

**Monthly limit exceeded:**
- System switches to fallback APIs automatically
- If all APIs exhausted, wait until next month

### Problem: Old jobs not being cleaned up

**Check cleanup is running:**
```bash
grep "Cleaning up old jobs" /home/firas/Utopia/logs/job_updater.log
```

**Manually clean up:**
```sql
DELETE FROM jobs WHERE posted_date < CURRENT_DATE - INTERVAL '30 days';
```

---

## 📊 Expected Database Growth

### Steady State (after 1 month)
```
New jobs daily:     ~30 jobs
Jobs removed daily: ~30 jobs (30 days old)
Net change:         ~0 (balanced)
Total in DB:        ~300-400 jobs (rolling 30 days)
```

### Growth Phase (first month)
```
Week 1:  ~150 jobs
Week 2:  ~300 jobs
Week 3:  ~450 jobs
Week 4:  ~600 jobs
Then stabilizes at ~300-400 (with cleanup)
```

---

## 🎉 Benefits

### For Users
✅ **Fresh Jobs Daily** - New opportunities every morning  
✅ **Diverse Coverage** - All regions and roles covered weekly  
✅ **Always Available** - 300-400 jobs always in database  
✅ **Recent Listings** - Jobs never older than 30 days  

### For You (Developer)
✅ **Zero Manual Work** - Fully automated  
✅ **No API Overages** - Smart budget management  
✅ **Easy Monitoring** - Comprehensive logs  
✅ **Reliable** - Automatic fallback on failures  

---

## 🔗 Quick Commands Reference

```bash
# Run daily update manually
python daily_job_updater.py

# Check API usage
python daily_job_updater.py --check-usage

# Setup automation
python daily_job_updater.py --setup-cron

# View logs
tail -f /home/firas/Utopia/logs/job_updater.log

# Edit crontab
crontab -e

# Check cron status
sudo systemctl status cron

# Database stats
psql -U postgres -d utopia_db -c "SELECT COUNT(*) FROM jobs;"
```

---

## 📞 Need Help?

**Check logs first:**
```bash
tail -100 /home/firas/Utopia/logs/job_updater.log
```

**Test manually:**
```bash
python daily_job_updater.py
```

**Verify APIs:**
```bash
python utils/job_scraper.py
```

---

## ✨ Summary

The Daily Job Updater gives you:

1. **Automated daily updates** (set and forget)
2. **Smart API management** (never run out)
3. **Fresh job listings** (30-day rolling window)
4. **Comprehensive coverage** (all regions, all roles)
5. **Easy monitoring** (logs + usage stats)

**Initial Setup (5 minutes):**
```bash
# 1. Setup automation
python daily_job_updater.py --setup-cron
crontab -e  # Add the cron line

# 2. Initial population (optional)
python quick_populate_jobs.py  # Seed with 300 jobs

# 3. Done! Jobs update daily at 2 AM
```

**Your database will always have 300-400 fresh jobs, updated automatically, without exhausting API limits!** 🎉
