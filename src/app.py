from flask import Flask, request, jsonify
from flask_cors import CORS
from Recommendation import load_data, recommend_movies
import sys
print(sys.path)
app = Flask(__name__)

app.config['WTF_CSRF_ENABLED'] = False


# Load data
movies_with_ratings = load_data()

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    genres = data.get('genres', [])
    min_rating = float(data.get('min_rating', 3.5))

    recommended = recommend_movies(movies_with_ratings, genres, min_rating=min_rating)

    if recommended.empty:
        return jsonify({'message': 'No recommendations found.'}), 404
    else:
        return jsonify(recommended[['title', 'average_rating', 'rating_count', 'genres']].to_dict(orient='records'))

if __name__ == '__main__':
    CORS(app)
    app.run(debug=False)
    
