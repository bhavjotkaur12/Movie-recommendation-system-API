from flask import Flask, request, jsonify
from flask_cors import CORS
from .Recommendation import load_data, recommend_movies

import sys
print(sys.path)
app = Flask(__name__)

app.config['WTF_CSRF_ENABLED'] = False

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>Movie Recommendation System</title>
        </head>
        <body>
            <h1>Welcome to the Movie Recommendation System</h1>
            <form action="/recommend" method="post">
                <label for="genres">Enter genres (comma-separated):</label>
                <input type="text" id="genres" name="genres"><br><br>
                <label for="min_rating">Minimum Rating:</label>
                <input type="text" id="min_rating" name="min_rating"><br><br>
                <input type="submit" value="Get Recommendations">
            </form>
        </body>
    </html>
    '''

# Load data
movies_with_ratings = load_data()

@app.route('/recommend', methods=['POST'])
@app.route('/recommend', methods=['POST'])
def recommend():
    # Access form data instead of JSON
    genres = request.form.get('genres', '').split(',')
    min_rating = request.form.get('min_rating', 3.5)
    try:
        min_rating = float(min_rating)
    except ValueError:
        return "Invalid minimum rating. Please enter a valid number.", 400

    recommended = recommend_movies(movies_with_ratings, genres, min_rating=min_rating)

    if recommended.empty:
        return jsonify({'message': 'No recommendations found.'}), 404
    else:
        return jsonify(recommended[['title', 'average_rating', 'rating_count', 'genres']].to_dict(orient='records'))

if __name__ == '__main__':
    CORS(app)
    app.run(debug=False)
    
