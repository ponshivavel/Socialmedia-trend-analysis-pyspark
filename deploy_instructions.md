# Production Deployment Instructions (Render.com)

## Single Backend Deploy (React + API)

**Why single deploy?** Flask serves React build + API = simpler architecture.

## Local Prep (Run These First):
```
npm install
npm run build
xcopy build backend\\static\\ /E /Y
xcopy data\\*.json backend\\data\\ /Y
```

## Render.com Settings (Exact):

**Service Type:** `Web Service`  
**Repository:** `ponshivavel/Socialmedia-trend-analysis-pyspark` (main branch)

**Root Directory:** `backend`

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn --bind 0.0.0.0:$PORT --workers 1 main:app
```

**Environment Variables:**
```
NEWS_API_KEY=83f001599a114bc1a2912f9ecdf660bb
PYTHON_VERSION=3.11
```

**Instance Type:** `Free` (testing) or `Starter $7/mo` (recommended)

## Deploy Flow:
```
1. render.com → New → Web Service → GitHub repo
2. Paste above settings 
3. Create → Live in 2-3 minutes!
4. URL: https://your-app.onrender.com
```

## Test Production Local:
```
cd backend
gunicorn --bind 0.0.0.0:10000 main:app
→ http://localhost:10000 (identical to Render)
```

**Result:** Live interactive social trends dashboard worldwide! 🌍📊
