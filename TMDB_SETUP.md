# TMDB API Setup Guide

To enable movie posters and additional details in the recommendation system, you need to get a free API key from The Movie Database (TMDB).

## Step 1: Get TMDB API Key

1. Go to [TMDB website](https://www.themoviedb.org/)
2. Create a free account or sign in
3. Go to your [Account Settings](https://www.themoviedb.org/settings/api)
4. Click on "API" in the left sidebar
5. Request an API key for "Developer" use
6. Fill out the form with your details
7. You'll receive your API key via email

## Step 2: Add API Key to App

1. Open `app.py`
2. Find this line:
   ```python
   TMDB_API_KEY = "your_tmdb_api_key_here"
   ```
3. Replace `"your_tmdb_api_key_here"` with your actual API key:
   ```python
   TMDB_API_KEY = "1234567890abcdef1234567890abcdef"
   ```

## Step 3: Alternative - Environment Variable

For better security, you can use an environment variable:

1. Create a `.env` file in your project directory:
   ```
   TMDB_API_KEY=your_actual_api_key_here
   ```

2. Modify the app.py to use environment variable:
   ```python
   import os
   TMDB_API_KEY = os.getenv("TMDB_API_KEY", "your_tmdb_api_key_here")
   ```

## Features Enabled with TMDB API

- 🎬 Movie posters for selected and recommended movies
- 📊 Real-time ratings and vote counts
- 📅 Release dates
- 📝 Movie overviews/descriptions
- 🎭 Genre information
- 📈 Popularity scores

## API Limits

- Free tier: 1,000 requests per day
- More than sufficient for personal use
- No cost involved

## Troubleshooting

If you see errors related to API calls:
1. Check if your API key is correct
2. Verify you have internet connection
3. Check if you've exceeded daily limits
4. Ensure the API key is properly formatted

The app will still work without the API key, but without posters and additional details. 