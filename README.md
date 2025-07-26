# Weather API Project

A complete example of transforming weather data into a free API using GitHub Actions.

## Features

- **Hourly weather updates** from wttr.in service
- **Current conditions** API endpoint
- **3-day forecast** API endpoint
- **Historical weather data** tracking
- **Interactive weather dashboard**
- **Completely free** hosting and automation

## 🚀 Live Demo

- **Current Weather API**: `https://raw.githubusercontent.com/username/weather-api-project/main/api/current.json`
- **Forecast API**: `https://raw.githubusercontent.com/username/weather-api-project/main/api/forecast.json`
- **Dashboard**: `https://username.github.io/weather-api-project/`

## 📊 API Endpoints

### Current Weather

```
GET https://raw.githubusercontent.com/username/weather-api-project/main/api/current.json
```

**Response:**

```json
{
  "location": "New York",
  "last_updated": "2025-07-26T12:00:00Z",
  "current": {
    "temperature_f": 75,
    "temperature_c": 24,
    "condition": "Partly Cloudy",
    "humidity": 65,
    "wind_speed_mph": 8,
    "wind_direction": "NW",
    "feels_like_f": 78,
    "uv_index": 6
  }
}
```

### 3-Day Forecast

```
GET https://raw.githubusercontent.com/username/weather-api-project/main/api/forecast.json
```

**Response:**

```json
{
  "location": "New York",
  "last_updated": "2025-07-26T12:00:00Z",
  "forecast": [
    {
      "date": "2025-07-26",
      "max_temp_f": 80,
      "min_temp_f": 65,
      "max_temp_c": 27,
      "min_temp_c": 18,
      "condition": "Sunny",
      "chance_of_rain": 10,
      "sunrise": "06:15 AM",
      "sunset": "07:45 PM"
    }
  ]
}
```

## ⚙️ Configuration

### Change Location

Edit `src/weather_scraper.py`:

```python
city = "London"  # Change to your preferred city
```

### Update Frequency

Modify `.github/workflows/hourly-weather.yml`:

```yaml
on:
  schedule:
    - cron: "0 * * * *" # Every hour (current)
    # - cron: "*/30 * * * *"  # Every 30 minutes
    # - cron: "0 */3 * * *"   # Every 3 hours
```

## 🎯 Use Cases

- **Mobile weather apps** - Free weather data API
- **IoT projects** - Weather data for sensors
- **Web dashboards** - Current conditions display
- **Home automation** - Weather-based triggers
- **Data analysis** - Historical weather patterns

## 🔧 Installation

1. **Fork this repository**
2. **Enable GitHub Actions** in repository settings
3. **Enable GitHub Pages** pointing to `/docs` folder
4. **Customize location** in `src/weather_scraper.py`
5. **Your weather API is live!**

## 📈 Dashboard Features

- Real-time weather display
- Temperature trends
- 3-day forecast cards
- Weather history charts
- Responsive design
- Auto-refresh every hour

## 🌐 Data Source

This project uses [wttr.in](https://wttr.in) - a console-oriented weather forecast service that provides free JSON API access.

## 🚨 Rate Limits

- **GitHub Actions**: 2,000 minutes/month (free tier)
- **API Requests**: No authentication required
- **Update Frequency**: Hourly recommended
- **Data Retention**: 30 days of history

## 📚 Documentation

Based on the [GitHub Data Platform Template](https://github.com/Joel-hanson/github-data-platform-template).

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## 📄 License

MIT License - Use for any purpose!

---

**Need a different location or update frequency?** Just fork and customize the configuration!
