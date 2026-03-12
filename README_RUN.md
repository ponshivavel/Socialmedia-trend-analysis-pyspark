
# Running the Social Media Trend Analysis Dashboard

## Prerequisites
- Node.js installed
- Python installed
- NewsAPI key (already configured: 83f001599a114bc1a2912f9ecdf660bb)

## Setup Steps

### 1. Backend Setup
Open a terminal and run:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup
Open another terminal and run:
```bash
npm start
```

### 3. Access the Dashboard
Open your browser at: http://localhost:3000

## Features

### Click Functionality:
- **Bar Chart (Trend Popularity)**: Click any bar to see full news articles related to that trend
- **Sentiment Chart**: Click any point to see news for that trend
  - Red points = Negative sentiment
  - Blue points = Positive sentiment

### Closing News Panel:
- Click the same bar/point again to close
- Click the X button in the modal
- Click outside the modal

### Region Filter:
- Use the dropdown to filter data by region

## API Endpoints:
- http://localhost:8000/trends/popularity - Get trend popularity data
- http://localhost:8000/trends/sentiment - Get sentiment data
- http://localhost:8000/trends/temporal - Get temporal trends
- http://localhost:8000/trends/geographical - Get geographical data
- http://localhost:8000/news?q=keyword - Get news by keyword
- http://localhost:8000/health - Health check

