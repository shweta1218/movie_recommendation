# 🎬 Movie Recommendation System

A modern, interactive movie recommender web app built with Streamlit. Get personalized movie recommendations, search and filter movies, and view real-time posters and details using the TMDB API.

## 🚀 Features
- Content-based movie recommendations
- Search and select movies with instant filtering
- Beautiful, responsive UI with dark mode
- Real movie posters and details via TMDB API
- Adjustable number of recommendations and similarity threshold
- Statistics and genre insights
- Easy setup and deployment

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/shweta1218/movie_recommendation.git
cd movie_recommendation
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. TMDB API Key Setup
- Get a free API key from [TMDB](https://www.themoviedb.org/settings/api)
- Set it as an environment variable:
  - On Windows:
    ```powershell
    $env:TMDB_API_KEY="your_tmdb_api_key_here"
    ```
  - On Mac/Linux:
    ```bash
    export TMDB_API_KEY="your_tmdb_api_key_here"
    ```
- Or edit `app.py` to paste your key directly (not recommended for production)

### 4. Run the app
```bash
streamlit run app.py
```

## 📦 Project Structure
```
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── movie_dict.pkl        # Movie data (preprocessed)
├── similarity.pkl        # Similarity matrix
├── tmdb_5000_movies.csv  # Raw movie data
├── tmdb_5000_credits.csv # Raw credits data
├── README.md             # This file
├── .gitignore            # Git ignore rules
```

## ✨ Credits
- [Streamlit](https://streamlit.io/)
- [TMDB API](https://www.themoviedb.org/documentation/api)
- Content-based filtering logic inspired by open datasets

## 📄 License
MIT License 
