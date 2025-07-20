# 🎬 Movie Recommendation System Using Python and Streamlit

A real-time movie recommendation web app built using the MovieLens dataset, collaborative filtering (cosine similarity), and TMDB API for fetching movie posters.

---

## 🚀 Features

- 🔍 Search any movie from the MovieLens dataset
- 🎯 Get top 5 similar movies based on user ratings
- 🖼️ Posters fetched dynamically via TMDB API
- 🧠 Cosine similarity-based collaborative filtering
- 🛠️ Simple UI built with Streamlit

---

## 📁 Dataset Used

- `movies.csv` – Movie titles and IDs  
- `ratings.csv` – User ratings for movies  
- `links.csv` – Maps MovieLens IDs to TMDB IDs  
- *(All files from [MovieLens 100k Dataset](https://grouplens.org/datasets/movielens/))*

---

## 🧠 How It Works

1. Creates a **user-item matrix** using pandas pivot table.
2. Computes **cosine similarity** between movies based on user ratings.
3. When a movie is selected, it finds top similar movies (excluding itself).
4. Merges results with `links.csv` to get TMDB IDs.
5. Fetches **movie posters** using TMDB API.

---

## 📦 Project Structure

## 🔧 Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Supriya15-btech/MovieRecommendationSystem
cd MovieRecommendationSystem
