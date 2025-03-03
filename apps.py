import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Book Recommendation System", page_icon="📚", layout="wide")

with open("books.pkl", "rb") as f:
    books = pickle.load(f)
with open("pt.pkl", "rb") as f:
    pt = pickle.load(f)
with open("similarity_score.pkl", "rb") as f:
    similarity_score = pickle.load(f)
with open("top_50.pkl", "rb") as f:
    popular_df = pickle.load(f)

if isinstance(books, dict):
    books = pd.DataFrame(books)
    
def recommend(book_name):
    if book_name not in pt.index:
        return []
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:9]
    
    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        if not temp_df.empty:
            item = [
                temp_df.iloc[0]['Book-Title'],
                temp_df.iloc[0]['Book-Author'],
                temp_df.iloc[0]['Image-URL-M']
            ]
            data.append(item)
    
    return data

st.sidebar.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #BEBEBE;
            border-radius: 15px;
            padding: 20px;
            width: 280px !important;
            min-width: 280px !important;
            max-width: 300px !important;
        }
        [data-testid="stSidebarNav"] {
            font-size: 24px;
            font-weight: bold;
            color: #2E3B55;
        }
        .stRadio > label {
            font-size: 22px !important;
            font-weight: bold;
            color: #4CAF50;
        }
    </style>
    """, unsafe_allow_html=True)


st.sidebar.title("Book Recommendation System")
option = st.sidebar.radio("Select an Option", ("Top 50 Books", "Book Recommender"))

# Top 50 Books Page
if option == "Top 50 Books":
    st.markdown("""
        <style>
            .top-books-header {
                text-align: center;
                color: white;
                font-size: 36px;
                background-color:rgb(25, 142, 55);
                padding: 15px;
                border-radius: 10px;
            }
            .divider {
                border: 2px solidrgb(236, 244, 237);
                margin-top: 10px;
            }
        </style>
        <h1 class='top-books-header'>📚 Top 50 Books</h1>
        <hr class='divider'>
    """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)  
    
    num_cols = 5
    num_books = len(popular_df)
    
    for i in range(0, num_books, num_cols):
        row_books = popular_df.iloc[i:i + num_cols]
        cols = st.columns(num_cols)
        
        for col, (_, row) in zip(cols, row_books.iterrows()):
            with col:
                st.image(row['Image-URL-M'], width=100)
                st.write(f"**{row['Book-Title']}**")
                st.write(row['Book-Author'])  
                st.write(f"Votes - {row['num_ratings']}")
                st.write(f"Rating - {row['avg_ratings']:.2f}")

# Book Recommendation Page
else:
    st.markdown("""
        <h1 style='text-align: center; color: black; background-color: #BEBEBE; padding: 10px;'>📚 Book Recommender</h1>
        <hr style='border: 2px solid #4CAF50;'>
    """, unsafe_allow_html=True)
    
    selected_book = st.selectbox("Select a book you like:", pt.index.tolist())
    
  # for button
    st.markdown("""
        <style>
            div.stButton > button:first-child {
                background-color: #4CAF50;
                color: black;
                font-size: 18px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 20px;
                transition: 0.3s;
            }
            div.stButton > button:first-child:hover {
                background-color:rgb(63, 169, 69);
            }
            
        </style>
    """, unsafe_allow_html=True)

    if st.button("Recommend"):
        st.session_state.button_clicked = True
        if st.session_state.button_clicked:
         st.markdown("""
        <style>
            div.stButton > button:first-child {
                color: black !important;
                background-color: #4CAF50 !important;
            }
        </style>
    """, unsafe_allow_html=True)
        recommendations = recommend(selected_book)
        st.write("### Recommended Books:")
        
        num_cols = 4
        num_books = len(recommendations)
        
        for i in range(0, num_books, num_cols):
            row_books = recommendations[i:i + num_cols]
            cols = st.columns(num_cols)
            
            for col, book in zip(cols, row_books):
                with col:
                    st.image(book[2], width=100)
                    st.write(f"**{book[0]}**")
                    st.write(book[1])
