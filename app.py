import pickle
import streamlit as st 
import requests

st.header("Movie Recommendation System")

# Load movie data and similarity matrix
movie = pickle.load(open(r'C:\Users\Admin\OneDrive\Desktop\Movie_recommendation_system\artificats\movie_list.pkl', 'rb'))
similarity = pickle.load(open(r'C:\Users\Admin\OneDrive\Desktop\Movie_recommendation_system\artificats\similarity.pkl', 'rb'))

movie_list = movie['title'].values
selected_movie = st.selectbox(
    'Type or select the movie to get recommendations',
    movie_list
)

def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=b7678f21d6374b768e6c3bfe0504a193&language=en-US".format(movie_id)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        poster_path = data['poster_path']
        poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path
        print(f"Poster URL for movie ID {movie_id}: {poster_url}")
        return poster_url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return ""  # Return an empty string if there's an error fetching the poster

def recommend(movie_df, similarity_matrix, selected_movie):
    index = movie_df[movie_df['title'] == selected_movie].index[0]
    distance = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distance[1:6]:
        movie_id = movie_df.iloc[i[0]]['movie_id']
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movie_posters.append(poster_url)
            recommended_movie_names.append(movie_df.iloc[i[0]]['title'])
    return recommended_movie_names, recommended_movie_posters

if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(movie, similarity, selected_movie)
    
    for i in range(min(5, len(recommended_movie_posters))):
        st.text(recommended_movie_names[i])
        st.image(recommended_movie_posters[i])
