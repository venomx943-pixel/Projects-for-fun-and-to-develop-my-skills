import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def secure_movie_recommendation(movie_title, movies_database, similarity_matrix):
    """
    Securely recommends similar movies based on content similarity 
    with rigorous input validation and safety checks.
    """
    # [Code Security & Vulnerability 1]: Type validation to prevent Type Confusion / Injection
    if not isinstance(movie_title, str):
        raise TypeError("Security Error: Movie title must be a string exclusively.")
    
    if not isinstance(movies_database, (list, np.ndarray)):
        raise TypeError("Security Error: Movies database must be a valid list or array.")

    # [Code Security & Vulnerability 2]: Maximum length constraint to prevent DoS via string overflow
    MAX_TITLE_LENGTH = 100
    if len(movie_title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Security Error: Movie title exceeds maximum length ({MAX_TITLE_LENGTH} chars).")

    # [Code Security & Vulnerability 3]: Search validity / Missing Index protection (Prevent out-of-bounds / KeyError)
    if movie_title not in movies_database:
        raise ValueError(f"Engineering Error: Movie '{movie_title}' not found in the database.")

    # [Data Structure & Algorithm]: Find index and extract cosine similarity scores O(n)
    movie_index = movies_database.index(movie_title)
    
    # Security check on matrix bounds
    if movie_index >= similarity_matrix.shape[0]:
        raise IndexError("Security Error: Index out of similarity matrix bounds.")

    similarity_scores = list(enumerate(similarity_matrix[movie_index]))
    
    # Sort scores in descending order (highest similarity first) using sorting algorithm O(n log n)
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Get top 2 recommendations (excluding the movie itself at index 0)
    top_recommendations = [movies_database[i[0]] for i in similarity_scores[1:3]]

    return top_recommendations

# Dummy database and similarity matrix initialization for testing
database = ["Action Hero", "Action Quest", "Romance in Paris", "Comedy Night"]
vectorizer = CountVectorizer()
count_matrix = vectorizer.fit_transform([
    "action hero fights evil", 
    "action quest and heroes", 
    "romance love in paris", 
    "comedy funny night"
])
sim_matrix = cosine_similarity(count_matrix)

user_query = "Action Hero"

try:
    recommendations = secure_movie_recommendation(user_query, database, sim_matrix)
    print(f"Secure Recommendations for '{user_query}': {recommendations}")
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")