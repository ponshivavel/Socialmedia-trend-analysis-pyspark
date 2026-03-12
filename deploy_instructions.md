# Production Deployment Instructions (Render.com)

## Single Backend Deploy (React + API)

**Why single deploy?** Flask serves React build + API = simpler architecture.

## Steps:

### 1. Build React
```
npm install
npm run build
```

### 2. Copy Data Files
```
copy data\*.json backend\data\
```

### 3. Create backend/.env
```
NEWS_API_KEY=83f001599a114bc1a2912f9ecdf660bb
```

### 4. Deploy to Render
```
1. render.com → New Web Service
2. Connect GitHub repo
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn backend.main:app`
5. Env: NEWS_API_KEY
```

**Result:** https://your-app.onrender.com → Full dashboard + API working

## Local Production Test
```
npm run build
python backend/main.py
localhost:10000 → Production-ready app
```

