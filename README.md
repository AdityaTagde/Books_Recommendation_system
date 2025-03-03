# 📚 Book Recommendation System

## 🌟 Overview
This is a book recommendation system built using Streamlit. It suggests books based on user input and displays the top 50 most popular books.

## 🚀 Features
- **Top 50 Books:** Displays a list of the 50 most popular books.
- **Book Recommender:** Suggests books similar to the one selected by the user.
-  **User-Friendly Interface:** Designed with an intuitive UI using Streamlit.

## 🛠 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/book-recommender.git
   cd book-recommender
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running the Application
Run the following command in your terminal:
```bash
streamlit run apps.py
```

## Dependencies
- Python
- Streamlit
- Pandas
- NumPy
- Pickle

## 📂 Files
- `apps.py` : Main application script.
- `books.pkl` 📚: Pickle file containing book data.
- `pt.pkl` : Pickle file with preprocessed data.
- `similarity_score.pkl` 📈: Pickle file containing similarity scores for recommendations.
- `top_50.pkl` : Pickle file containing the top 50 most popular books.

## 🎯 Usage
1. Open the web app in your browser after running the command.
2. Use the sidebar to select between "Top 50 Books" and "Book Recommender."
3. If you select "Top 50 Books":
   - A list of the most popular books will be displayed.
   - Each book will include its title, author, cover image, number of ratings, and average rating.
4. If you select "Book Recommender":
   - A dropdown menu will appear where you can select a book you like.
   - Click the "Recommend" button to generate a list of similar books.
   - The recommended books will be displayed with their titles, authors, and cover images.
5. Browse the recommendations and explore new books based on your preferences.

