# UtopiaHire - Quick Start

## Run the Project (No Setup Required)

### 1. Install Docker
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac)
- Or `sudo apt install docker.io docker-compose` (Linux)

### 2. Get a Groq API Key
- Sign up at https://console.groq.com
- Create an API key (free tier available)

### 3. Run
```bash
# Download the compose file
curl -O https://raw.githubusercontent.com/Talent-Bridge-hub/team-xyz/main/docker-compose.yml

# Start (replace YOUR_KEY with your Groq API key)
GROQ_API_KEY=YOUR_KEY docker compose up -d
```

### 4. Access
- **Frontend:** http://localhost:3000
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### 5. Stop
```bash
docker compose down
```

---

## That's it! 🎉
Database auto-configures, no manual setup needed.
