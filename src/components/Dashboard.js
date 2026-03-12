
import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

const Dashboard = () => {
  const [popularityData, setPopularityData] = useState([]);
  const [sentimentData, setSentimentData] = useState([]);
  const [temporalData, setTemporalData] = useState([]);
  const [geographicalData, setGeographicalData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRegion, setSelectedRegion] = useState('');
  const [selectedTrend, setSelectedTrend] = useState(null);
  const [newsData, setNewsData] = useState([]);
  const [newsLoading, setNewsLoading] = useState(false);

  const regions = [
    { value: '', label: 'All Regions' },
    { value: 'Worldwide', label: 'Worldwide' },
    { value: 'United States', label: 'United States' },
    { value: 'India', label: 'India' },
    { value: 'United Kingdom', label: 'United Kingdom' },
    { value: 'Canada', label: 'Canada' },
    { value: 'Australia', label: 'Australia' },
    { value: 'Germany', label: 'Germany' },
    { value: 'France', label: 'France' },
    { value: 'Japan', label: 'Japan' },
    { value: 'South Korea', label: 'South Korea' }
  ];

  const fetchData = useCallback(async () => {
    try {
      const popularityUrl = selectedRegion
        ? `http://localhost:8000/trends/popularity?region=${encodeURIComponent(selectedRegion)}`
        : 'http://localhost:8000/trends/popularity';

      const sentimentUrl = selectedRegion
        ? `http://localhost:8000/trends/sentiment?region=${encodeURIComponent(selectedRegion)}`
        : 'http://localhost:8000/trends/sentiment';

      const temporalUrl = selectedRegion
        ? `http://localhost:8000/trends/temporal?region=${encodeURIComponent(selectedRegion)}`
        : 'http://localhost:8000/trends/temporal';

      const geographicalUrl = 'http://localhost:8000/trends/geographical';

      const [popularityRes, sentimentRes, temporalRes, geographicalRes] = await Promise.all([
        axios.get(popularityUrl),
        axios.get(sentimentUrl),
        axios.get(temporalUrl),
        axios.get(geographicalUrl)
      ]);

      setPopularityData(popularityRes.data);
      setSentimentData(sentimentRes.data);
      setTemporalData(temporalRes.data);
      setGeographicalData(geographicalRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  }, [selectedRegion]);

  const fetchNews = async (keyword) => {
    setNewsLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/news?q=${encodeURIComponent(keyword)}`);
      setNewsData(response.data.articles || []);
    } catch (error) {
      console.error('Error fetching news:', error);
      setNewsData([]);
    } finally {
      setNewsLoading(false);
    }
  };

  const handleBarClick = (event) => {
    if (!event.points || !event.points[0]) return;
    
    const clickedTrend = event.points[0].x;
    
    if (selectedTrend === clickedTrend) {
      // Close news panel if same trend clicked
      setSelectedTrend(null);
      setNewsData([]);
    } else {
      // Open news panel for new trend
      setSelectedTrend(clickedTrend);
      fetchNews(clickedTrend);
    }
  };

  const handleSentimentClick = (event) => {
    if (!event.points || !event.points[0]) return;
    
    const clickedTrend = event.points[0].x;
    
    if (selectedTrend === clickedTrend) {
      // Close news panel if same trend clicked
      setSelectedTrend(null);
      setNewsData([]);
    } else {
      // Open news panel for new trend
      setSelectedTrend(clickedTrend);
      fetchNews(clickedTrend);
    }
  };

  const closeNewsPanel = () => {
    setSelectedTrend(null);
    setNewsData([]);
  };

  useEffect(() => {
    fetchData();
  }, [selectedRegion, fetchData]);

  if (loading) {
    return <div className="dashboard">Loading...</div>;
  }

  // Prepare sentiment colors - red for negative, blue for positive
  const sentimentColors = sentimentData.map(d => d.sentiment < 0 ? 'rgb(220,53,69)' : 'rgb(0,123,255)');

  return (
    <div className="dashboard">
      <header>
        <h1>Social Media Trend Analysis Dashboard</h1>
        <div className="header-controls">
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="region-select"
          >
            {regions.map(region => (
              <option key={region.value} value={region.value}>
                {region.label}
              </option>
            ))}
          </select>
        </div>
      </header>

      <div className="chart-container">
        <h2>Trend Popularity</h2>
        <Plot
          data={[
            {
              type: 'bar',
              x: popularityData.map(d => d.trend),
              y: popularityData.map(d => d.mentions),
              name: 'Mentions',
              marker: {
                color: popularityData.map(d => 
                  selectedTrend === d.trend ? '#ffc107' : 'rgb(54, 162, 235)'
                )
              }
            }
          ]}
          layout={{
            title: 'Top Trending Topics (Click to see news)',
            xaxis: { title: 'Trend' },
            yaxis: { title: 'Mentions' },
            clickmode: 'event+select'
          }}
          onClick={handleBarClick}
        />
      </div>

      <div className="chart-container">
        <h2>Sentiment Analysis</h2>
        <Plot
          data={[
            {
              type: 'scatter',
              mode: 'markers',
              x: sentimentData.map(d => d.trend),
              y: sentimentData.map(d => d.sentiment),
              name: 'Sentiment Score',
              marker: {
                size: 12,
                color: sentimentColors,
                line: {
                  color: 'white',
                  width: 1
                }
              }
            }
          ]}
          layout={{
            title: 'Sentiment Distribution (Red = Negative, Blue = Positive, Click to see news)',
            xaxis: { title: 'Trend', tickangle: -45 },
            yaxis: { title: 'Sentiment (-1 to 1)' },
            clickmode: 'event+select'
          }}
          onClick={handleSentimentClick}
        />
      </div>

      <div className="chart-container">
        <h2>Temporal Trends</h2>
        <Plot
          data={[
            {
              type: 'line',
              x: temporalData.map(d => d.timestamp),
              y: temporalData.map(d => d.trend_count),
              name: 'Trend Count'
            }
          ]}
          layout={{
            title: 'Trends Over Time',
            xaxis: { title: 'Time' },
            yaxis: { title: 'Number of Trends' }
          }}
        />
      </div>

      <div className="chart-container">
        <h2>Geographical Sentiment Map</h2>
        <Plot
          data={[
            // Country-level choropleth
            {
              type: 'choropleth',
              locations: geographicalData.filter(d => d.type === 'country').map(d => d.country_code),
              z: geographicalData.filter(d => d.type === 'country').map(d => d.sentiment),
              text: geographicalData.filter(d => d.type === 'country').map(d => `${d.region}: ${d.sentiment} sentiment (${d.count} trends)`),
              colorscale: [
                [0, 'rgb(165,0,38)'],
                [0.25, 'rgb(215,48,39)'],
                [0.5, 'rgb(244,109,67)'],
                [0.75, 'rgb(253,174,97)'],
                [1, 'rgb(254,224,144)']
              ],
              colorbar: {
                title: 'Sentiment Score',
                titleside: 'right'
              },
              showscale: true
            },
            // City-level scatter points
            {
              type: 'scattergeo',
              mode: 'markers+text',
              lat: geographicalData.filter(d => d.type === 'city').map(d => d.lat),
              lon: geographicalData.filter(d => d.type === 'city').map(d => d.lon),
              text: geographicalData.filter(d => d.type === 'city').map(d => `${d.region}: ${d.sentiment} (${d.count} trends)`),
              marker: {
                size: geographicalData.filter(d => d.type === 'city').map(d => Math.max(d.count * 2, 8)),
                color: geographicalData.filter(d => d.type === 'city').map(d => d.sentiment),
                colorscale: [
                  [0, 'rgb(165,0,38)'],
                  [0.25, 'rgb(215,48,39)'],
                  [0.5, 'rgb(244,109,67)'],
                  [0.75, 'rgb(253,174,97)'],
                  [1, 'rgb(254,224,144)']
                ],
                showscale: false,
                opacity: 0.8
              },
              textposition: 'top center',
              textfont: {
                size: 10
              }
            }
          ]}
          layout={{
            title: 'Global Sentiment Analysis by Region',
            geo: {
              showframe: false,
              showcoastlines: true,
              projection: {
                type: 'natural earth'
              }
            },
            showlegend: false
          }}
        />
      </div>

      {/* News Panel Modal */}
      {selectedTrend && (
        <div className="news-modal-overlay" onClick={closeNewsPanel}>
          <div className="news-modal" onClick={(e) => e.stopPropagation()}>
            <div className="news-modal-header">
              <h2>News for: {selectedTrend}</h2>
              <button className="close-btn" onClick={closeNewsPanel}>&times;</button>
            </div>
            <div className="news-modal-content">
              {newsLoading ? (
                <div className="news-loading">Loading news...</div>
              ) : newsData.length > 0 ? (
                <div className="news-list">
                  {newsData.map((article, index) => (
                    <div key={index} className="news-item">
                      {article.urlToImage && (
                        <img 
                          src={article.urlToImage} 
                          alt={article.title} 
                          className="news-image"
                          onError={(e) => e.target.style.display = 'none'}
                        />
                      )}
                      <h3>{article.title}</h3>
                      <p className="news-description">{article.description}</p>
                      <div className="news-meta">
                        <span>{article.source}</span>
                        <span>{article.publishedAt ? new Date(article.publishedAt).toLocaleDateString() : ''}</span>
                      </div>
                      <a href={article.url} target="_blank" rel="noopener noreferrer" className="read-more">
                        Read Full Article
                      </a>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="no-news">No news found for this trend.</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

