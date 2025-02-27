# -*- coding: utf-8 -*-
"""movie_recommendation_system.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Eb4eWPFRqM7e0ersGcGrO7KJk2Oi0LLp
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

"""Loading the datasets"""

movies=pd.read_csv('movies.csv')
credits=pd.read_csv('credits.csv')

"""Data Preprocessing"""

credits.head()

movies.head()

movies.columns

credits.columns

movies.shape, credits.shape

# renaming the movie_id column to id
credits_new=credits.rename(columns={'movie_id':'id'})

# merging or combining both datasets
movies_merge=movies.merge(credits_new, on='id')

movies_merge.head(1)

movies_merge.shape

movies.columns

movies_merge.info()

# dropping the irrelevant columns from the dataset
df=movies_merge.drop(columns=['homepage', 'title_x', 'title_y', 'status','production_countries'])

df.info()

# counting the number of movies of each language
movies_merge['original_language'].value_counts()

# making a new dataframe by taking important features
movies=movies_merge[['id','original_title','overview','genres','keywords','cast','crew']]

movies.head()

# checking null values
movies.isnull().sum()

# removing null values
movies.dropna(inplace=True)

movies.isnull().sum()

# checking duplicates
movies.duplicated().sum()

movies.iloc[0].genres

# ['Action','Adventure','Fantasy','Sci-Fi']

import ast
def convert(obj):
  l=[]
  for i in ast.literal_eval(obj):
    l.append(i['name'])
  return l

# converting the dictionary form of genres into list
movies['genres']=movies['genres'].apply(convert)

movies.head()

# coverting keywords dictionary into list
movies['keywords']=movies['keywords'].apply(convert)

def convert3(obj):
  l=[]
  coounter=0
  for i in ast.literal_eval(obj):
    if coounter!=3:
      l.append(i['name'])
      coounter+=1
    else:
      break
  return l

# converting cast dict into list
movies['cast']=movies['cast'].apply(convert)

movies.head()

def director(obj):
  l=[]
  for i in ast.literal_eval(obj):
    if i['job']=='Director':
      l.append(i['name'])
      break
  return l

# getting directors from the crew column
movies['crew']=movies['crew'].apply(director)

movies.head()

# converting overview into list
movies['overview']=movies['overview'].apply(lambda x:x.split())

movies.head()

# removing spaces between words
movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head(1)

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

movies.head(1)

df=movies[['id','original_title','tags']]

df.head(1)

# converting the tags column data type  into string
df['tags']=df['tags'].apply(lambda x:" ".join(x))

# converting tags column into lower case
df['tags']=df['tags'].apply(lambda x:x.lower())

df.head()

df.shape

"""TEXT VECTORIZATION"""

df['tags'][0]

from sklearn.feature_extraction.text import TfidfVectorizer
tf=TfidfVectorizer(max_features=5000, stop_words='english')

vect=tf.fit_transform(df['tags']).toarray()

vectors=tf.fit_transform(df['tags']).toarray().shape

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

stem('in the 22nd century, a paraplegic marine is dispatched to the moon pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. action adventure fantasy sciencefiction cultureclash future spacewar spacecolony society spacetravel futuristic romance space alien tribe alienplanet cgi marine soldier battle loveaffair antiwar powerrelations mindandsoul 3d samworthington zoesaldana sigourneyweaver stephenlang michellerodriguez giovanniribisi joeldavidmoore cchpounder wesstudi lazalonso dileeprao mattgerald seananthonymoran jasonwhyte scottlawrence kellykilgour jamespatrickpitt seanpatrickmurphy peterdillon kevindorman kelsonhenderson davidvanhorn jacobtomuri michaelblain-rozgay joncurry lukehawker woodyschultz petermensah soniayee jahnelcurfman ilramchoi kylawarren lisaroumain debrawilson chrismala taylorkibby jodielandau julielamm cullenb.madden josephbradymadden frankietorres austinwilson sarawilson tamicawashington-miller lucybriant nathanme')

df['tags']=df['tags'].apply(stem)

df.head(1)

from sklearn.metrics.pairwise import cosine_similarity

# Assuming vectors is a tuple containing the shape (4800, 5000)
# And the actual data is stored in the variable 'vect'

# Recalculate the cosine similarity using the 'vect' variable
cosine_similarity_matrix = cosine_similarity(vect)

# Print the shape of the cosine similarity matrix
print(cosine_similarity_matrix.shape)

# main function using tfidf vectorizer

def recommend1(movie):
  # Filter for the movie title, ignoring case
  movie_rows = df[df['original_title'].str.lower() == movie.lower()]

  # Check if any rows were found
  if movie_rows.empty:
    print(f"Movie '{movie}' not found in the dataset.")
    return

  # Get the index of the first matching row
  movie_index = movie_rows.index[0]

  distances = cosine_similarity_matrix[movie_index]
  movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

  for i in movies_list:
    print(df.iloc[i[0]].original_title)

recommend1('avatar')

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer as cv

# Assuming 'df' contains your movie data and 'tags' column

# 1. Create a CountVectorizer instance
cvz = cv(max_features=5000, stop_words='english')

# 2. Fit and transform the 'tags' column to get the vector representation
vector = cvz.fit_transform(df['tags']).toarray()

# 3. Calculate the cosine similarity matrix using the 'vector'
cos_sim_2 = cosine_similarity(vector)  # Use cosine_similarity function, not the matrix

# Now 'cos_sim_2' will contain the new cosine similarity matrix based on 'vector'

print(cos_sim_2)

# main functon using count vectorizer
def recommend2(movie):
  # Filter for the movie title, ignoring case
  movie_rows = df[df['original_title'].str.lower() == movie.lower()]

  # Check if any rows were found
  if movie_rows.empty:
    print(f"Movie '{movie}' not found in the dataset.")
    return

  # Get the index of the first matching row
  movie_index = movie_rows.index[0]

  distances = cos_sim_2[movie_index]
  movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

  for i in movies_list:
    print(df.iloc[i[0]].original_title)

recommend2('avatar')

import pickle

pickle.dump(df.to_dict(), open('movies_dict.pkl', 'wb'))

pickle.dump(cosine_similarity_matrix, open('similarity.pkl', 'wb') )

