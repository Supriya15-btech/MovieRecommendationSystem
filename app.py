import pandas as pd
import streamlit as st
import requests
from sklearn.metrics.pairwise import cosine_similarity

# ───── CONFIG ─────
API_KEY = "655cd46e371556fda16a80af0d13daf7"
PLACEHOLDER = "https://via.placeholder.com/342x513?text=No+Poster"

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

# ───── Load Data ─────
@st.cache_data(show_spinner=False)
def load_data():
    def read_csv_safe(path):
        for enc in ("utf-8", "utf-8-sig", "cp1252", "latin1"):
            try:
                return pd.read_csv(path, encoding=enc, engine="python", on_bad_lines="warn")
            except:
                continue
        raise Exception(f"Cannot read {path}")

    movies = read_csv_safe("movies.csv")
    ratings = read_csv_safe("ratings.csv")
    links = read_csv_safe("links.csv")

    if "rating" not in ratings.columns:
        st.error("❌ 'rating' column missing in ratings.csv.")
        st.stop()

    return movies, ratings, links

movies, ratings, links = load_data()

# ───── Cosine Similarity Matrix ─────
@st.cache_data(show_spinner=False)
def build_similarity_matrix(ratings_df):
    pivot = ratings_df.pivot_table(index='movieId', columns='userId', values='rating').fillna(0)
    sim = cosine_similarity(pivot)
    return pd.DataFrame(sim, index=pivot.index, columns=pivot.index)

similarity_df = build_similarity_matrix(ratings)

# ───── Poster Fetching ─────
def fetch_poster_by_tmdb_id(tmdb_id):
    if pd.isna(tmdb_id):
        return PLACEHOLDER
    try:
        url = f"https://api.themoviedb.org/3/movie/{int(tmdb_id)}"
        params = {"api_key": API_KEY, "language": "en-US"}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if data.get("poster_path"):
            return f"https://image.tmdb.org/t/p/w342{data['poster_path']}"
    except Exception as e:
        print(f"[Poster error for TMDB ID {tmdb_id}]: {e}")
    return PLACEHOLDER

# ───── Recommend Movies ─────
def recommend(movie_title, k=6):
    match = movies[movies["title"] == movie_title]
    if match.empty:
        return pd.DataFrame()

    movie_id = match.iloc[0]["movieId"]
    if movie_id not in similarity_df.columns:
        return pd.DataFrame()

    similar_ids = similarity_df[movie_id].sort_values(ascending=False).iloc[1:50].index
    recommended = movies[movies["movieId"].isin(similar_ids)]

    # Match movieId types
    links["movieId"] = links["movieId"].astype(int)
    recommended["movieId"] = recommended["movieId"].astype(int)

    # Merge with links.csv to get tmdbId
    recommended = recommended.merge(links[['movieId', 'tmdbId']], on='movieId', how='left')

    # ✅ Skip movies with missing tmdbId
    recommended = recommended.dropna(subset=['tmdbId'])

    return recommended.head(k)

# ───── Streamlit UI ─────
selected = st.selectbox("🔍 Choose a movie", movies["title"].sort_values())

if st.button("🎯 Recommend"):
    results = recommend(selected)

    if results.empty:
        st.warning("No recommendations found.")
    else:
        st.success(f"Because you watched **{selected}**…")
        cols = st.columns(len(results))

        for col, (_, row) in zip(cols, results.iterrows()):
            with col:
                poster = fetch_poster_by_tmdb_id(row["tmdbId"])
                st.image(poster, use_container_width=True)
                st.caption(row["title"])
