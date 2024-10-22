import requests
from flask import Blueprint, request, jsonify
from collections import Counter
import random

recommendationAPI = Blueprint('recommendationAPI', __name__)

# Helper function to get restaurant data by ID
def get_restaurant_by_id(restaurant_id):
    url = f"https://restaurantservice-375afbe356dc.herokuapp.com/restaurant/{restaurant_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('cuisine_type', None)
    return None

# Helper function to get a list of restaurants by cuisine_type
def get_restaurants_by_cuisine(cuisine_type):
    url = f"https://restaurantservice-375afbe356dc.herokuapp.com/restaurant/list/{cuisine_type}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Assumes it returns a list of restaurants
    return []

@recommendationAPI.route('/<string:user_id>', methods=['GET'])
def get_user_recomendations(user_id):
    # Step 1: Get user's visit history
    history_url = f"https://history-service-7d9c8283d538.herokuapp.com/history/{user_id}"
    history_response = requests.get(history_url)
    
    if history_response.status_code != 200:
        return jsonify({"error": "Could not retrieve history"}), 500
    
    history_data = history_response.json()

    # Step 2: Extract restaurant_ids and find the top 3 most frequent (moda)
    restaurant_ids = [visit['restaurant_id'] for visit in history_data]
    restaurant_counts = Counter(restaurant_ids)
    top_3_restaurants = [restaurant for restaurant, count in restaurant_counts.most_common(3)]
    
    # Step 3: Get the cuisine_type for the top 3 restaurants
    cuisine_types = []
    for restaurant_id in top_3_restaurants:
        cuisine_type = get_restaurant_by_id(restaurant_id)
        if cuisine_type:
            cuisine_types.append(cuisine_type)
    
    # Step 4: Get 2 random restaurants for each cuisine_type
    final_recommendations = []
    for cuisine_type in cuisine_types:
        restaurants = get_restaurants_by_cuisine(cuisine_type)
        if restaurants:
            selected_restaurants = random.sample(restaurants, min(2, len(restaurants)))  # Get 2 random restaurants
            final_recommendations.extend(selected_restaurants)
    
    # Step 5: Return the final list of 6 restaurants
    return jsonify(final_recommendations), 200
