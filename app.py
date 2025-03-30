import streamlit as st
import pickle
import requests
import time
from tmdbv3api import TMDb
from tmdbv3api import Movie

def fetch_poster(movie_id):
    tmdb = TMDb()
    tmdb.api_key = '61758edf407739556c13c4cdc712062c'  # Set your API key
    movie = Movie()
    try:
        movie_details = movie.details(movie_id)
        poster_path = movie_details['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except Exception as e:
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return "https://unsplash.com/photos/clapboard-camera-and-copy-space-on-white-background-1878GCQTo08"

def fetch_poster1(movie_id):
    # url = "https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1M2YzNDFhMDU1NWVhNTY4NzBhYjQ0MzVlOWQ0NDIxZSIsIm5iZiI6MTc0MzMxNjk2OC4wMzgsInN1YiI6IjY3ZThlN2U4NzAwYTZhOTRjNmU1NDE4ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._W01IJ-3EiN1GBxXr7D4k0QQt_k7EZ6u1oPUoVyi7jk"
    }
    time.sleep(1)
    url = "https://api.themoviedb.org/3/movie/{}?api_key=61758edf407739556c13c4cdc712062c&language=en-US".format(movie_id)
    data = requests.get(url, headers=headers)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movie_posters

movies = pickle.load(open('movie_list.pkl', 'rb'))
movie_titles = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender')

selected_movie = st.selectbox(
    'Which movies do you watch?',
    movie_titles
)

if st.button('Recommend'):
    recommended_movies,recommended_movie_posters = recommend(selected_movie)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movie_posters[4])
