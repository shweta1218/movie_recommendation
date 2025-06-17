import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
import io
import os

# Page configuration
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .movie-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        margin-bottom: 0.5rem;
        word-wrap: break-word;
    }
    
    .movie-rating {
        color: #FFD700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .movie-genres {
        color: #E0E0E0;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .recommendation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .poster-container {
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .poster-image {
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .poster-image:hover {
        transform: scale(1.05);
    }

    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .loading {
        text-align: center;
        padding: 2rem;
        color: #667eea;
    }
    
    .error-message {
        background: #ff6b6b;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #51cf66;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .api-warning {
        background: #ffa726;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #ff9800;
    }
    
    /* Fix for empty containers */
    .stColumn > div:empty {
        display: none;
    }
    
    /* Better spacing for recommendation cards */
    .recommendation-section {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    /* Ensure consistent card heights */
    .movie-card-content {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    
    .movie-card-footer {
        margin-top: auto;
    }
</style>
""", unsafe_allow_html=True)

# TMDB API configuration - Try to get from environment variable first
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "f0930e240f95119977b59e75dfee82da")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Check if API key is properly set
API_KEY_AVAILABLE = TMDB_API_KEY != "your_tmdb_api_key_here" and TMDB_API_KEY != ""

def get_movie_poster(movie_title):
    """Get movie poster from TMDB API"""
    if not API_KEY_AVAILABLE:
        return None
        
    try:
        # Search for movie
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            'api_key': TMDB_API_KEY,
            'query': movie_title,
            'language': 'en-US',
            'page': 1
        }
        
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            if poster_path:
                return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
        
        return None
    except Exception as e:
        st.error(f"Error fetching poster for {movie_title}: {str(e)}")
        return None

def get_movie_details(movie_title):
    """Get additional movie details from TMDB"""
    if not API_KEY_AVAILABLE:
        return None
        
    try:
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            'api_key': TMDB_API_KEY,
            'query': movie_title,
            'language': 'en-US',
            'page': 1
        }
        
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data['results']:
            movie = data['results'][0]
            return {
                'overview': movie.get('overview', ''),
                'release_date': movie.get('release_date', ''),
                'vote_average': movie.get('vote_average', 0),
                'vote_count': movie.get('vote_count', 0),
                'popularity': movie.get('popularity', 0),
                'poster_path': movie.get('poster_path', '')
            }
        
        return None
    except Exception as e:
        return None

def recommend(movie):
    """Get movie recommendations"""
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            movie_id = i[0]
            movie_title = movies.iloc[i[0]].title
            similarity_score = i[1]
            
            # Get additional details
            details = get_movie_details(movie_title)
            
            recommended_movies.append({
                'title': movie_title,
                'similarity': similarity_score,
                'details': details
            })
        
        return recommended_movies
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return []

# Load data
@st.cache_data
def load_data():
    try:
        movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
        movies_df = pd.DataFrame(movie_dict)
        similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
        return movies_df, similarity_matrix
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

# Load data
movies, similarity = load_data()

if movies is None or similarity is None:
    st.error("Failed to load movie data. Please check if the pickle files exist.")
    st.stop()

# Main app
st.markdown('<h1 class="main-header">🎬 Movie Recommender System</h1>', unsafe_allow_html=True)

# Show API warning if key is not available
if not API_KEY_AVAILABLE:
    st.markdown("""
    <div class="api-warning">
        <strong>⚠️ TMDB API Key Not Configured</strong><br>
        Movie posters and additional details are not available. 
        To enable them, please set up your TMDB API key. 
        See <code>TMDB_SETUP.md</code> for instructions.
    </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎛️ Settings")
    
    # Number of recommendations
    num_recommendations = st.slider(
        "Number of Recommendations",
        min_value=3,
        max_value=10,
        value=5,
        step=1
    )
    
    # Minimum similarity threshold
    min_similarity = st.slider(
        "Minimum Similarity Score",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.05
    )
    
    # Show posters toggle (only if API key is available)
    if API_KEY_AVAILABLE:
        show_posters = st.checkbox("Show Movie Posters", value=True)
    else:
        show_posters = False
        st.info("Posters disabled - API key not configured")
    
    # Show details toggle
    show_details = st.checkbox("Show Movie Details", value=True)
    
    st.markdown("---")
    
    # Statistics
    st.header("📊 Statistics")
    st.metric("Total Movies", len(movies))
    
    # Genre distribution
    if 'genres' in movies.columns:
        all_genres = []
        for genres in movies['genres']:
            if isinstance(genres, list):
                all_genres.extend(genres)
        
        genre_counts = pd.Series(all_genres).value_counts().head(10)
        st.write("**Top Genres:**")
        for genre, count in genre_counts.items():
            st.write(f"• {genre}: {count}")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    st.subheader("🔍 Search & Select Movie")
    
    # Search functionality
    search_term = st.text_input(
        "Search movies:",
        placeholder="Type movie name to search...",
        help="Start typing to filter movies"
    )
    
    # Filter movies based on search
    if search_term:
        filtered_movies = movies[movies['title'].str.contains(search_term, case=False, na=False)]
        if len(filtered_movies) == 0:
            st.warning("No movies found matching your search.")
            movie_options = movies['title'].values
        else:
            movie_options = filtered_movies['title'].values
    else:
        movie_options = movies['title'].values
    
    # Movie selection
    selected_movie_name = st.selectbox(
        "Choose a movie:",
        movie_options,
        index=0 if len(movie_options) > 0 else None
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if selected_movie_name:
        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
        st.subheader("📽️ Selected Movie")
        
        # Get movie details
        movie_details = get_movie_details(selected_movie_name)
        
        if movie_details and show_posters and movie_details['poster_path']:
            poster_url = f"{TMDB_IMAGE_BASE_URL}{movie_details['poster_path']}"
            st.image(poster_url, width=200, caption=selected_movie_name)
        elif not API_KEY_AVAILABLE:
            st.info("🎬 Movie poster not available (API key needed)")
        
        st.markdown(f'<div class="movie-title">{selected_movie_name}</div>', unsafe_allow_html=True)
        
        if movie_details:
            st.markdown(f'<div class="movie-rating">⭐ Rating: {movie_details["vote_average"]:.1f}/10</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="movie-genres">📅 Released: {movie_details["release_date"]}</div>', unsafe_allow_html=True)
            
            if show_details and movie_details['overview']:
                st.write("**Overview:**")
                st.write(movie_details['overview'][:200] + "...")
        elif not API_KEY_AVAILABLE:
            st.info("📊 Additional details not available (API key needed)")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Recommendation button
st.markdown("---")
if st.button("🎯 Get Recommendations", type="primary", use_container_width=True):
    if selected_movie_name:
        with st.spinner("Finding the best recommendations for you..."):
            recommendations = recommend(selected_movie_name)
            
            if recommendations:
                st.markdown('<h2 class="main-header">🎬 Recommended Movies</h2>', unsafe_allow_html=True)
                
                # Filter by similarity threshold
                filtered_recommendations = [
                    rec for rec in recommendations 
                    if rec['similarity'] >= min_similarity
                ]
                
                if filtered_recommendations:
                    st.markdown('<div class="recommendation-section">', unsafe_allow_html=True)
                    
                    # Calculate optimal number of columns based on recommendations
                    num_recommendations = len(filtered_recommendations)
                    
                    if num_recommendations <= 3:
                        cols = st.columns(num_recommendations)
                    else:
                        cols = st.columns(3)  # Maximum 3 columns
                    
                    # Display recommendations
                    for idx, rec in enumerate(filtered_recommendations):
                        if num_recommendations <= 3:
                            col_idx = idx
                        else:
                            col_idx = idx % 3
                        
                        with cols[col_idx]:
                            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                            
                            # Show poster if available
                            if show_posters and rec['details'] and rec['details']['poster_path']:
                                poster_url = f"{TMDB_IMAGE_BASE_URL}{rec['details']['poster_path']}"
                                st.image(poster_url, width=150, caption=rec['title'])
                            elif not API_KEY_AVAILABLE:
                                st.info("🎬 Poster not available")
                            
                            st.markdown(f'<div class="movie-title">{rec["title"]}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="movie-rating">📊 Similarity: {rec["similarity"]:.3f}</div>', unsafe_allow_html=True)
                            
                            if rec['details']:
                                st.markdown(f'<div class="movie-rating">⭐ Rating: {rec["details"]["vote_average"]:.1f}/10</div>', unsafe_allow_html=True)
                                
                                if show_details and rec['details']['overview']:
                                    st.write("**Overview:**")
                                    st.write(rec['details']['overview'][:100] + "...")
                            elif not API_KEY_AVAILABLE:
                                st.info("📊 Details not available")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning(f"No movies found with similarity >= {min_similarity}")
            else:
                st.error("No recommendations found. Please try a different movie.")
    else:
        st.warning("Please select a movie first!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p>🎬 Movie Recommendation System powered by AI</p>
        <p>Built with Streamlit • Enhanced with TMDB API</p>
    </div>
    """,
    unsafe_allow_html=True
)
