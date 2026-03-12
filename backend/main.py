from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import json
import glob
from datetime import datetime
from dotenv import load_dotenv

# Load .env from backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__, static_folder="../build", static_url_path="/")

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Helper function to get latest data file
def get_latest_data_file():
    """Get the latest data file, preferring latest.json"""
    latest_file = "data/processed_data_latest.json"
    if os.path.exists(latest_file):
        return latest_file
    processed_files = glob.glob("data/processed_data_*.json")
    if not processed_files:
        return None
    return max(processed_files)


@app.route("/api/trends/popularity")
def get_popularity_trends():
    """Get trend popularity data, optionally filtered by region"""
    try:
        region = request.args.get('region')
        latest_file = get_latest_data_file()
        if not latest_file:
            return jsonify([])
        
        with open(latest_file, 'r') as f:
            data = json.load(f)

        popularity_data = data.get("popularity", [])

        if region:
            popularity_data = [item for item in popularity_data if item.get('region') == region]

        return jsonify(popularity_data)
    except Exception as e:
        return jsonify({"error": f"Error fetching data: {str(e)}"}), 500


@app.route("/api/trends/sentiment")
def get_sentiment_trends():
    """Get sentiment analysis data, optionally filtered by region"""
    try:
        region = request.args.get('region')
        latest_file = get_latest_data_file()
        if not latest_file:
            return jsonify([])
        
        with open(latest_file, 'r') as f:
            data = json.load(f)

        sentiment_data = data.get("sentiment", [])

        if region:
            sentiment_data = [item for item in sentiment_data if item.get('region') == region]

        return jsonify(sentiment_data)
    except Exception as e:
        return jsonify({"error": f"Error fetching data: {str(e)}"}), 500


@app.route("/api/trends/temporal")
def get_temporal_trends():
    """Get temporal trend patterns, optionally filtered by region"""
    try:
        region = request.args.get('region')
        latest_file = get_latest_data_file()
        if not latest_file:
            return jsonify([])

        with open(latest_file, 'r') as f:
            data = json.load(f)

        temporal_data = data.get("temporal", [])

        if region:
            temporal_data = [item for item in temporal_data if item.get('region') == region]

        return jsonify(temporal_data)
    except Exception as e:
        return jsonify({"error": f"Error fetching data: {str(e)}"}), 500


@app.route("/api/trends/geographical")
def get_geographical_trends():
    """Get geographical trend data with sentiment by region"""
    try:
        latest_file = get_latest_data_file()
        if not latest_file:
            return jsonify([])

        with open(latest_file, 'r') as f:
            data = json.load(f)
     
        sentiment_data = data.get("sentiment", [])

        # Aggregate sentiment by region
        region_sentiment = {}
        for item in sentiment_data:
            region = item.get('region', 'Unknown')
            sentiment = float(item.get('sentiment', 0))
            if region not in region_sentiment:
                region_sentiment[region] = {'total_sentiment': 0, 'count': 0}
            region_sentiment[region]['total_sentiment'] += sentiment
            region_sentiment[region]['count'] += 1

        # Calculate average sentiment per region and get coordinates
        geographical_data = []
        country_codes = {
            'United States': 'USA',
            'United Kingdom': 'GBR',
            'India': 'IND',
            'Canada': 'CAN',
            'Australia': 'AUS',
            'Germany': 'DEU',
            'France': 'FRA',
            'Japan': 'JPN',
            'South Korea': 'KOR',
            'Brazil': 'BRA'
        }

        # City/state coordinates for specific locations
        location_coords = {
            'New York': {'lat': 40.7128, 'lon': -74.0060},
            'Los Angeles': {'lat': 34.0522, 'lon': -118.2437},
            'Chicago': {'lat': 41.8781, 'lon': -87.6298},
            'London': {'lat': 51.5074, 'lon': -0.1278},
            'Paris': {'lat': 48.8566, 'lon': 2.3522},
            'Berlin': {'lat': 52.5200, 'lon': 13.4050},
            'Tokyo': {'lat': 35.6762, 'lon': 139.6503},
            'Sydney': {'lat': -33.8688, 'lon': 151.2093},
            'Toronto': {'lat': 43.6532, 'lon': -79.3832},
            'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
            'Delhi': {'lat': 28.7041, 'lon': 77.1025},
            'Bangalore': {'lat': 12.9716, 'lon': 77.5946},
            'Seoul': {'lat': 37.5665, 'lon': 126.9780},
            'São Paulo': {'lat': -23.5505, 'lon': -46.6333},
            'Rio de Janeiro': {'lat': -22.9068, 'lon': -43.1729}
        }

        for region, values in region_sentiment.items():
            avg_sentiment = values['total_sentiment'] / values['count'] if values['count'] > 0 else 0

            if region in location_coords:
                coords = location_coords[region]
                geographical_data.append({
                    'region': region,
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'sentiment': round(avg_sentiment, 2),
                    'count': values['count'],
                    'type': 'city'
                })
            else:
                country_code = country_codes.get(region, '')
                geographical_data.append({
                    'region': region,
                    'country_code': country_code,
                    'sentiment': round(avg_sentiment, 2),
                    'count': values['count'],
                    'type': 'country'
                })

        return jsonify(geographical_data)
    except Exception as e:
        return jsonify({"error": f"Error fetching data: {str(e)}"}), 500


# Helper function to get sample news when API is rate limited
def get_sample_news(keyword):
    """Return sample news articles when API is rate limited"""
    if not keyword:
        keyword = "trending"
    
    sample_articles = [
        {
            "title": f"Latest developments in {keyword} - Analysis and Updates",
            "description": f"Comprehensive coverage of {keyword} with expert analysis and latest updates from around the world.",
            "url": f"https://example.com/news/{keyword.lower()}-1",
            "urlToImage": None,
            "publishedAt": datetime.now().isoformat(),
            "source": "Sample News"
        },
        {
            "title": f"{keyword} Impact on Global Markets",
            "description": f"How {keyword} is affecting markets and what experts predict for the future.",
            "url": f"https://example.com/news/{keyword.lower()}-2",
            "urlToImage": None,
            "publishedAt": datetime.now().isoformat(),
            "source": "Sample News"
        },
        {
            "title": f"Breaking: {keyword} Updates and Analysis",
            "description": f"Latest breaking news and analysis on {keyword} from our correspondents worldwide.",
            "url": f"https://example.com/news/{keyword.lower()}-3",
            "urlToImage": None,
            "publishedAt": datetime.now().isoformat(),
            "source": "Sample News"
        },
        {
            "title": f"What experts say about {keyword}",
            "description": f"Expert opinions and analysis on {keyword} and its implications.",
            "url": f"https://example.com/news/{keyword.lower()}-4",
            "urlToImage": None,
            "publishedAt": datetime.now().isoformat(),
            "source": "Sample News"
        }
    ]
    return sample_articles


@app.route("/api/news")
def get_news():
    """Get news articles, optionally filtered by query and region"""
    try:
        import requests
        
        q = request.args.get('q')
        region = request.args.get('region')
        
        # Use top-headlines endpoint which has higher rate limits
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'apiKey': os.getenv("NEWS_API_KEY"),
            'pageSize': 20,
            'language': 'en'
        }
        
        # Use query if provided, otherwise get general top headlines
        if q:
            params['q'] = q
        elif region and region not in ['Worldwide', '']:
            # Map region to country code for top-headlines
            country_map = {
                'United States': 'us', 'United Kingdom': 'gb', 'India': 'in',
                'Canada': 'ca', 'Australia': 'au', 'Germany': 'de',
                'France': 'fr', 'Japan': 'jp', 'South Korea': 'kr', 'Brazil': 'br'
            }
            country_code = country_map.get(region)
            if country_code:
                params['country'] = country_code
            else:
                params['country'] = 'us'
        else:
            params['country'] = 'us'  # Default to US
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('articles', [])
        
        # If no articles from API (rate limited), return sample data
        if not articles:
            return jsonify({
                "totalResults": 0,
                "articles": get_sample_news(q or "trending"),
                "note": "API rate limited, showing sample news"
            })
        
        return jsonify({
            "totalResults": data.get('totalResults', 0),
            "articles": [
                {
                    "title": article.get('title'),
                    "description": article.get('description'),
                    "url": article.get('url'),
                    "urlToImage": article.get('urlToImage'),
                    "publishedAt": article.get('publishedAt'),
                    "source": article.get('source', {}).get('name')
                }
                for article in articles if article.get('title') and article.get('title') != '[Removed]'
            ]
        })
    except Exception as e:
        # Return sample news on error
        return jsonify({
            "totalResults": 0,
            "articles": get_sample_news(q or "trending"),
            "error": str(e)
        })


@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route("/")
def home():
    """Home route for backend availability check"""
    return "Backend is running successfully"


# Serve React app for all other routes
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    """Serve React app"""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

