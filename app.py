from urllib import response

import streamlit as st
import pandas as pd
import pickle
import requests
import os
# Recommend movies based on cosine_similarity ---main fun
def recommend(movie):
        movie_rows = movies[movies['original_title'].str.lower() == movie.lower()]

        # Check if any rows were found
        if movie_rows.empty:
            print(f"Movie '{movie}' not found in the dataset.")
            return

        # Get the index of the first matching row
        movie_index = movie_rows.index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        rec_mov=[]
        for i in movies_list:
            movies_id=i[0]
            rec_mov.append(movies.iloc[i[0]].original_title)
        return rec_mov
st.title('Movie Recommendation System')
movies_dict=pickle.load(open('movies_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)
movies_dict=movies_dict['original_title'].values
similarity=pickle.load(open('similarity.pkl','rb'))

selected_movie_name=st.selectbox(
    'Select the movie',
    (movies['original_title'].values)
)
if st.button("Recommend"):
        titles = recommend(selected_movie_name)
        for i in titles:
            st.write(i)