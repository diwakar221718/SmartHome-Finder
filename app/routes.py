from flask import Blueprint, render_template, request
import pandas as pd

from app.prediction import predict_price
from app.recommendation import recommend_properties
from app.utils import calculate_accessibility

main = Blueprint('main', __name__)

# load dataset
df = pd.read_csv('data/combined_final_dataset.csv')

cities = sorted(df['City'].dropna().unique())


@main.route('/', methods=['GET'])
def home():
    return render_template('index.html', cities=cities)


@main.route('/predict', methods=['POST'])
def predict():

    try:
        # ----------------------------
        # 1. Get form data + validation
        # ----------------------------
        city = request.form.get('city')
        
        if not city:
            return render_template('index.html', cities=cities, error="Please select a city")

        bhk = max(1, int(request.form.get('bhk', 1)))
        bathrooms = max(1, int(request.form.get('bathrooms', 1)))
        balconies = max(0, int(request.form.get('balconies', 0)))
        area = max(100, float(request.form.get('area', 1000)))
        age = max(0, int(request.form.get('age', 0)))
        amenities = max(0, int(request.form.get('amenities', 0)))

        # budget in lakhs → INR
        budget = float(request.form.get('budget', 50)) * 100000

        sort_by = request.form.get('sort', 'match')

        # ----------------------------
        # 2. City → coordinates
        # ----------------------------
        city_data = df[df['City'] == city]

        if city_data.empty:
            lat, lon = 28.6139, 77.2090  # fallback (Delhi)
        else:
            lat = city_data['Latitude'].mean()
            lon = city_data['Longitude'].mean()

        # ----------------------------
        # 3. Accessibility
        # ----------------------------
        access_score = calculate_accessibility(city, lat, lon)

        # ----------------------------
        # 4. User input (IMPORTANT)
        # ----------------------------
        user_input = {
            'City': city,   # 🔥 IMPORTANT (for filtering)
            'BHK': bhk,
            'Bathrooms': bathrooms,
            'Balconies': balconies,
            'CarpetArea_sqft': area,
            'AgeYears': age,
            'AmenitiesCount': amenities,
            'Latitude': lat,
            'Longitude': lon,
            'AccessibilityScore': access_score
        }

        # ----------------------------
        # 5. Price Prediction
        # ----------------------------
        price_data = predict_price(user_input)
        predicted_price = price_data["predicted_price"]

        # ----------------------------
        # 6. Affordability
        # ----------------------------
        affordability_score = budget / predicted_price

        if affordability_score >= 1:
            affordability_label = "Affordable ✅"
        elif affordability_score >= 0.8:
            affordability_label = "Slightly Expensive ⚠️"
        else:
            affordability_label = "Expensive ❌"

        # ----------------------------
        # 7. Recommendations
        # ----------------------------
        recommendations = recommend_properties(user_input, budget)

        # ----------------------------
        # 8. EDGE CASE: no results
        # ----------------------------
        if len(recommendations) == 0:
            return render_template(
                'results.html',
                price=price_data,
                results=[],
                city=city,
                affordability=round(affordability_score, 2),
                affordability_label=affordability_label
            )

        # ----------------------------
        # 9. SORTING (FIXED PROPERLY)
        # ----------------------------
        if sort_by == "area":
            recommendations = sorted(
                recommendations,
                key=lambda x: x.get('CarpetArea_sqft', 0),
                reverse=True
            )

        elif sort_by == "match":
            recommendations = sorted(
                recommendations,
                key=lambda x: x.get('MatchPercent', 0),
                reverse=True
            )

        elif sort_by == "price":
            recommendations = sorted(
                recommendations,
                key=lambda x: x.get('Price_INR', 0)
            )

        elif sort_by == "affordability":
            recommendations = sorted(
                recommendations,
                key=lambda x: x.get('AffordabilityScore', 0),
                reverse=True
            )

        # ----------------------------
        # 10. Render
        # ----------------------------
        return render_template(
            'results.html',
            price=price_data,
            results=recommendations,
            city=city,
            affordability=round(affordability_score, 2),
            affordability_label=affordability_label
        )
    
    except Exception as e:
        return render_template('index.html', cities=cities, error=f"An error occurred: {str(e)}")