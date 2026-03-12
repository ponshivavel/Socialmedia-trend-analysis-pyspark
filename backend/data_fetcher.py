"""
News Data Fetcher and Processor
Fetches news from NewsAPI and processes them for trend analysis
"""
import requests
import json
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict
import glob

# Load API key
from dotenv import load_dotenv
import pathlib

# Load .env from backend directory
env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    raise ValueError("NEWS_API_KEY not found in environment variables")

# Regions to fetch news from
REGIONS = [
    "United States", "United Kingdom", "India", "Canada", "Australia",
    "Germany", "France", "Japan", "South Korea", "Brazil"
]

CITIES = [
    "New York", "Los Angeles", "Chicago", "London", "Paris", "Berlin",
    "Tokyo", "Sydney", "Toronto", "Mumbai", "Delhi", "Bangalore",
    "Seoul", "São Paulo", "Rio de Janeiro"
]

# Stop words to filter out (common words that are not meaningful trends)
STOP_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
    'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up',
    'about', 'into', 'over', 'after', 'beneath', 'under', 'above',
    'the', 'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either',
    'neither', 'not', 'only', 'own', 'same', 'than', 'too', 'very',
    'just', 'also', 'now', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'any', 'this', 'that', 'these',
    'those', 'it', 'its', 'he', 'she', 'they', 'them', 'his', 'her',
    'their', 'what', 'which', 'who', 'whom', 'whose', 'i', 'me', 'my',
    'we', 'us', 'our', 'you', 'your', 'said', 'says', 'say', 'will',
    'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can',
    'new', 'one', 'two', 'first', 'last', 'day', 'time', 'year', 'like',
    'make', 'made', 'get', 'got', 'go', 'went', 'come', 'came', 'take',
    'took', 'see', 'saw', 'know', 'knew', 'think', 'thought', 'want',
    'use', 'find', 'give', 'tell', 'try', 'call', 'look', 'seem', 'leave',
    'put', 'keep', 'let', 'begin', 'began', 'show', 'showed', 'hear',
    'heard', 'play', 'run', 'move', 'live', 'believe', 'bring', 'happen',
    'write', 'provide', 'sit', 'stand', 'lose', 'pay', 'meet', 'include',
    'continue', 'set', 'learn', 'change', 'lead', 'understand', 'watch',
    'follow', 'stop', 'create', 'speak', 'read', 'allow', 'add', 'spend',
    'grow', 'open', 'walk', 'win', 'offer', 'remember', 'love', 'consider',
    'appear', 'buy', 'wait', 'serve', 'die', 'send', 'expect', 'build',
    'stay', 'fall', 'cut', 'reach', 'kill', 'remain', 'suggest', 'raise',
    'pass', 'sell', 'require', 'report', 'decide', 'pull', 'develop'
}

# Keyword-based sentiment dictionary
POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome',
    'positive', 'success', 'successful', 'happy', 'joy', 'love', 'best', 'better',
    'growth', 'increase', 'rise', 'improve', 'improvement', 'win', 'winner',
    'achievement', 'breakthrough', 'innovation', 'innovative', 'revolutionary',
    'historic', 'hope', 'optimistic', 'prosperity', 'strong', 'strength'
}

NEGATIVE_WORDS = {
    'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst', 'worse', 'negative',
    'fail', 'failure', 'sad', 'angry', 'hate', 'crisis', 'disaster', 'accident',
    'death', 'die', 'dead', 'kill', 'attack', 'terror', 'war', 'conflict',
    'recession', 'decline', 'drop', 'fall', 'loss', 'lose', 'bankruptcy',
    'scandal', 'fraud', 'corruption', 'abuse', 'violence', 'crime', 'criminal',
    'pollution', 'climate', 'danger', 'threat', 'warning', 'emergency'
}


def fetch_news(query=None, region=None, page_size=100):
    """Fetch news from NewsAPI"""
    url = "https://newsapi.org/v2/top-headlines"
    
    params = {
        'apiKey': API_KEY,
        'pageSize': page_size,
        'language': 'en'
    }
    
    if query:
        params['q'] = query
    if region:
        # Map region to country code
        country_map = {
            'United States': 'us', 'United Kingdom': 'gb', 'India': 'in',
            'Canada': 'ca', 'Australia': 'au', 'Germany': 'de',
            'France': 'fr', 'Japan': 'jp', 'South Korea': 'kr', 'Brazil': 'br'
        }
        country_code = country_map.get(region)
        if country_code:
            params['country'] = country_code
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('articles', [])
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []


def extract_keywords(text):
    """Extract keywords from text (hashtags and capitalized words), filtering out stop words"""
    if not text:
        return []
    
    # Extract hashtags
    hashtags = re.findall(r'#(\w+)', text)
    
    # Extract capitalized words (potential proper nouns)
    capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
    
    # Filter out stop words
    all_keywords = [kw for kw in (hashtags + capitalized) if kw.lower() not in STOP_WORDS]
    
    return list(set(all_keywords))


def calculate_sentiment(text):
    """Calculate sentiment score based on keywords"""
    if not text:
        return 0
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    positive_count = sum(1 for word in words if word in POSITIVE_WORDS)
    negative_count = sum(1 for word in words if word in NEGATIVE_WORDS)
    
    total = positive_count + negative_count
    if total == 0:
        return 0
    
    return (positive_count - negative_count) / total


def simulate_temporal_data(articles, region):
    """Simulate temporal trend patterns"""
    temporal_data = []
    
    # Extract keywords from all articles
    all_keywords = []
    for article in articles:
        title = article.get('title', '') or ''
        description = article.get('description', '') or ''
        all_keywords.extend(extract_keywords(title + ' ' + description))
    
    # Count keyword occurrences
    keyword_counts = defaultdict(int)
    for keyword in all_keywords:
        keyword_counts[keyword] += 1
    
    # Get top keywords
    top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Simulate 24-hour pattern with peaks
    peak_hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]  # Business hours
    
    for keyword, count in top_keywords:
        for hour in range(24):
            # Simulate volume based on hour
            base_volume = count * 10
            if hour in peak_hours:
                volume = base_volume * (1.5 + (hour - 9) * 0.1)
            else:
                volume = base_volume * 0.5
            
            temporal_data.append({
                'region': region,
                'keyword': keyword,
                'hour': hour,
                'volume': int(volume),
                'mentions': count
            })
    
    return temporal_data


def process_news():
    """Main function to fetch and process news data"""
    print("Starting news data fetch and processing...")
    
    all_popularity = []
    all_sentiment = []
    all_temporal = []
    
    # Fetch news for each region
    for region in REGIONS:
        print(f"Fetching news for {region}...")
        articles = fetch_news(region=region)
        
        if not articles:
            # Try with a query fallback
            articles = fetch_news(query=region.split()[0], region=region)
        
        print(f"  Found {len(articles)} articles")
        
        # Process articles for popularity
        keyword_counts = defaultdict(int)
        keyword_sentiments = defaultdict(list)
        
        for article in articles:
            title = article.get('title', '') or ''
            description = article.get('description', '') or ''
            content = article.get('content', '') or ''
            
            keywords = extract_keywords(title + ' ' + description + ' ' + content)
            sentiment = calculate_sentiment(title + ' ' + description + ' ' + content)
            
            for keyword in keywords:
                keyword_counts[keyword] += 1
                keyword_sentiments[keyword].append(sentiment)
        
        # Add to popularity data
        for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:8]:
            avg_sentiment = sum(keyword_sentiments[keyword]) / len(keyword_sentiments[keyword]) if keyword_sentiments[keyword] else 0
            
            all_popularity.append({
                'platform': 'NewsAPI',
                'trend': keyword,
                'mentions': count,
                'avg_volume': float(count * 1.5),
                'max_volume': float(count * 2.5),
                'region': region
            })
            
            all_sentiment.append({
                'platform': 'NewsAPI',
                'trend': keyword,
                'sentiment': round(avg_sentiment, 3),
                'region': region
            })
        
        # Generate temporal data
        temporal_region = simulate_temporal_data(articles, region)
        all_temporal.extend(temporal_region)
    
    # Also fetch for major cities
    for city in CITIES:
        if city not in REGIONS:  # Avoid duplicates
            print(f"Fetching news for {city}...")
            articles = fetch_news(query=city)
            print(f"  Found {len(articles)} articles")
            
            # Process similar to regions
            keyword_counts = defaultdict(int)
            keyword_sentiments = defaultdict(list)
            
            for article in articles:
                title = article.get('title', '') or ''
                description = article.get('description', '') or ''
                content = article.get('content', '') or ''
                
                keywords = extract_keywords(title + ' ' + description + ' ' + content)
                sentiment = calculate_sentiment(title + ' ' + description + ' ' + content)
                
                for keyword in keywords:
                    keyword_counts[keyword] += 1
                    keyword_sentiments[keyword].append(sentiment)
            
            for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                avg_sentiment = sum(keyword_sentiments[keyword]) / len(keyword_sentiments[keyword]) if keyword_sentiments[keyword] else 0
                
                all_popularity.append({
                    'platform': 'NewsAPI',
                    'trend': keyword,
                    'mentions': count,
                    'avg_volume': float(count * 1.5),
                    'max_volume': float(count * 2.5),
                    'region': city
                })
                
                all_sentiment.append({
                    'platform': 'NewsAPI',
                    'trend': keyword,
                    'sentiment': round(avg_sentiment, 3),
                    'region': city
                })
    
    # Create data directory if not exists
    os.makedirs('data', exist_ok=True)
    
    # Save processed data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'data/processed_data_{timestamp}.json'
    
    processed_data = {
        'popularity': all_popularity,
        'sentiment': all_sentiment,
        'temporal': all_temporal,
        'fetched_at': datetime.now().isoformat()
    }
    
    with open(output_file, 'w') as f:
        json.dump(processed_data, f, indent=2)
    
    print(f"Data saved to {output_file}")
    print(f"Total popularity entries: {len(all_popularity)}")
    print(f"Total sentiment entries: {len(all_sentiment)}")
    print(f"Total temporal entries: {len(all_temporal)}")
    
    return output_file


if __name__ == "__main__":
    process_news()

