# Backend Architecture - Complete Explanation

## 🏗️ Backend Overview

Your backend has 4 main modules:

```
app/
├── __init__.py      → Flask app factory
├── routes.py        → API endpoints (main logic)
├── prediction.py    → ML price prediction
├── recommendation.py → Property recommendation
└── utils.py         → Utility functions
```

---

## 1️⃣ MAIN.PY - Entry Point

```python
from app import create_app
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
```

**What it does:**
- Imports Flask app factory
- Creates app instance
- Starts server on port 5000

---

## 2️⃣ APP/__INIT__.PY - Flask App Factory

```python
from flask import Flask
import os

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app
```

**What it does:**
- Creates Flask app with correct folder paths
- Tells Flask where templates (HTML) are
- Tells Flask where static files (CSS/JS) are
- Registers routes/blueprints

---

## 3️⃣ APP/ROUTES.PY - Main Controller

This handles all user requests. Two main routes:

### Route 1: Home Page (GET /)
```python
@main.route('/', methods=['GET'])
def home():
    return render_template('index.html', cities=cities)
```

**Flow:**
```
User visits localhost:5000
    ↓
GET / request
    ↓
Renders index.html with city list
    ↓
User sees search form
```

---

### Route 2: Prediction (POST /predict)

This is the **main business logic**:

```python
@main.route('/predict', methods=['POST'])
def predict():
    try:
        # STEP 1: Get & validate form data
        city = request.form.get('city')
        bhk = max(1, int(request.form.get('bhk', 1)))
        bathrooms = max(1, int(request.form.get('bathrooms', 1)))
        area = max(100, float(request.form.get('area', 1000)))
        budget = float(request.form.get('budget', 50)) * 100000
        
        # STEP 2: Get city coordinates
        city_data = df[df['City'] == city]
        if city_data.empty:
            lat, lon = 28.6139, 77.2090  # Delhi fallback
        else:
            lat = city_data['Latitude'].mean()
            lon = city_data['Longitude'].mean()
        
        # STEP 3: Calculate accessibility
        access_score = calculate_accessibility(city, lat, lon)
        
        # STEP 4: Create user input object
        user_input = {
            'City': city,
            'BHK': bhk,
            'Bathrooms': bathrooms,
            'CarpetArea_sqft': area,
            'Latitude': lat,
            'Longitude': lon,
            'AccessibilityScore': access_score
        }
        
        # STEP 5: Predict price
        price_data = predict_price(user_input)
        predicted_price = price_data["predicted_price"]
        
        # STEP 6: Calculate affordability
        affordability_score = budget / predicted_price
        if affordability_score >= 1:
            affordability_label = "Affordable ✅"
        elif affordability_score >= 0.8:
            affordability_label = "Slightly Expensive ⚠️"
        else:
            affordability_label = "Expensive ❌"
        
        # STEP 7: Get recommendations
        recommendations = recommend_properties(user_input, budget)
        
        # STEP 8: Sort results
        if sort_by == "area":
            recommendations = sorted(recommendations, 
                key=lambda x: x.get('CarpetArea_sqft', 0), reverse=True)
        elif sort_by == "match":
            recommendations = sorted(recommendations,
                key=lambda x: x.get('MatchPercent', 0), reverse=True)
        
        # STEP 9: Render results
        return render_template(
            'results.html',
            price=price_data,
            results=recommendations,
            city=city,
            affordability=round(affordability_score, 2),
            affordability_label=affordability_label
        )
    
    except Exception as e:
        return render_template('index.html', cities=cities, 
                             error=f"Error: {str(e)}")
```

**Complete Flow:**
```
User submits form
    ↓
Validate inputs (bhk ≥ 1, area ≥ 100, etc.)
    ↓
Get city center coordinates
    ↓
Calculate accessibility score
    ↓
Create user_input dictionary
    ↓
Call predict_price() → Get predicted price
    ↓
Calculate affordability (budget / price)
    ↓
Call recommend_properties() → Get top 5 properties
    ↓
Sort by user preference (match%, area, price)
    ↓
Render results.html with all data
```

---

## 4️⃣ APP/PREDICTION.PY - ML Price Prediction

```python
import joblib
import numpy as np
import pandas as pd

model = joblib.load('models/model.pkl')
scaler = joblib.load('models/scaler.pkl')
features = joblib.load('models/features.pkl')

def predict_price(user_input):
    # Convert dict to DataFrame
    input_df = pd.DataFrame([user_input])
    
    # Align columns with trained model
    input_df = input_df.reindex(columns=features, fill_value=0)
    
    # Scale features (normalize)
    input_scaled = scaler.transform(input_df)
    
    # Predict using Random Forest
    pred = model.predict(input_scaled)[0]
    
    # Calculate confidence interval
    tree_preds = [tree.predict(input_scaled)[0] for tree in model.estimators_]
    mean = np.mean(tree_preds)
    std = np.std(tree_preds)
    
    return {
        "predicted_price": round(pred),
        "lower": round(mean - std),
        "upper": round(mean + std)
    }
```

**What it does:**

1. **Load pre-trained models**
   - model.pkl: Random Forest trained on property data
   - scaler.pkl: Feature normalizer
   - features.pkl: List of feature names

2. **Convert input to DataFrame**
   ```python
   user_input = {'BHK': 2, 'Area': 1200, ...}
   input_df = pd.DataFrame([user_input])
   ```

3. **Align features**
   - Ensures columns match trained model
   - Fills missing columns with 0

4. **Scale features**
   - Normalizes to same scale
   - Important for ML accuracy

5. **Make prediction**
   - Random Forest predicts price

6. **Calculate confidence interval**
   - Gets predictions from all 100 trees
   - Calculates mean and std deviation
   - Lower = mean - std, Upper = mean + std

**Example:**
```
Input: 2 BHK, 1200 sqft, Delhi
    ↓
Scaled features
    ↓
Random Forest predicts: ₹50,00,000
    ↓
Tree predictions: [49,50,000, 50,10,000, 49,90,000, ...]
    ↓
Mean: 50,00,000, Std: 1,00,000
    ↓
Return: {
    "predicted_price": 5000000,
    "lower": 4900000,
    "upper": 5100000
}
```

---

## 5️⃣ APP/RECOMMENDATION.PY - Recommendation Engine

```python
def recommend_properties(user_input, budget, top_n=5):
    
    # STEP 1: FILTERING
    df_filtered = df[df["City"] == user_city]
    df_filtered = df_filtered[
        (df_filtered["CarpetArea_sqft"] >= 0.8 * user_area) &
        (df_filtered["CarpetArea_sqft"] <= 1.2 * user_area)
    ]
    df_filtered = df_filtered[
        df_filtered["BHK"].between(user_bhk - 1, user_bhk + 1)
    ]
    df_filtered = df_filtered[
        df_filtered["Price_INR"] <= 1.2 * budget
    ]
    
    # STEP 2: FEATURE WEIGHTING
    weights = np.ones(len(features))
    for i, f in enumerate(features):
        if f == "BHK": weights[i] = 3
        elif "Area" in f: weights[i] = 3
        elif f == "Bathrooms": weights[i] = 2
        elif f == "AccessibilityScore": weights[i] = 2
    
    # STEP 3: SIMILARITY CALCULATION
    data_scaled = scaler.transform(df_filtered[features])
    user_scaled = scaler.transform(user_df)
    
    data_scaled *= weights
    user_scaled *= weights
    
    sim = cosine_similarity(user_scaled, data_scaled)[0]
    
    # STEP 4: SCORING
    result['SimilarityScore'] = raw_scores
    result['AffordabilityScore'] = budget / result['Price_INR']
    result['AccessibilityScore'] = calculate_accessibility(...)
    
    result['FinalScore'] = (
        0.5 * (result['SimilarityScore'] * 100) +
        0.3 * (result['AffordabilityScore'] * 100) +
        0.2 * (result['AccessibilityScore'] * 100)
    )
    result['FinalScore'] += result['BHK_Bonus']
    
    # STEP 5: RANKING
    result = result.sort_values(by='FinalScore', ascending=False)
    result = result.head(top_n)
    
    return result.to_dict(orient='records')
```

**What it does:**

1. **Filter properties**
   - By city, area (±20%), BHK (±1), budget (≤120%)

2. **Weight features**
   - BHK: 3 (most important)
   - Area: 3 (most important)
   - Bathrooms: 2
   - Accessibility: 2

3. **Calculate similarity**
   - Cosine similarity between user and properties
   - Weighted by importance

4. **Multi-factor scoring**
   - Similarity (50%) + Affordability (30%) + Accessibility (20%)
   - Add BHK bonus if matches

5. **Rank and return**
   - Sort by final score
   - Return top 5

---

## 6️⃣ APP/UTILS.PY - Utility Functions

```python
from geopy.distance import geodesic

landmarks = {
    "Delhi": {
        "metro": [(28.6139, 77.2090), ...],
        "hospital": [(28.5672, 77.2100), ...]
    },
    ...
}

def calculate_accessibility(city, lat, lon):
    if city not in landmarks:
        return 0.5
    
    min_distances = []
    
    for category in landmarks[city].values():
        dists = [
            geodesic((lat, lon), coord).km
            for coord in category
        ]
        min_distances.append(min(dists))
    
    avg_dist = sum(min_distances) / len(min_distances)
    score = 1 / (1 + avg_dist)
    
    return round(score, 3)
```

**What it does:**

1. **Get landmark coordinates** for city
2. **Calculate distance** to nearest metro and hospital
3. **Average distances**
4. **Calculate accessibility score**
   - Formula: 1 / (1 + avg_distance)
   - Higher score = better accessibility

**Example:**
```
City: Delhi, Lat: 28.6139, Lon: 77.2090
    ↓
Nearest metro: 2.5 km
Nearest hospital: 1.8 km
    ↓
Average: 2.15 km
    ↓
Score = 1 / (1 + 2.15) = 0.317
```

---

## 📊 Complete Backend Flow

```
User submits form (index.html)
    ↓
POST /predict request
    ↓
routes.py: predict() function
    ├─ Validate inputs
    ├─ Get city coordinates
    ├─ Call utils.py: calculate_accessibility()
    ├─ Call prediction.py: predict_price()
    │   └─ Load ML model
    │   └─ Scale features
    │   └─ Predict price
    │   └─ Calculate confidence interval
    ├─ Calculate affordability
    ├─ Call recommendation.py: recommend_properties()
    │   ├─ Filter properties
    │   ├─ Calculate similarity
    │   ├─ Multi-factor scoring
    │   └─ Return top 5
    ├─ Sort results
    └─ Render results.html
        ↓
User sees recommendations
```

---

## 🔑 Key Backend Concepts

### 1. **Request-Response Cycle**
```
User Request → Flask Route → Processing → Response (HTML)
```

### 2. **Data Flow**
```
Form Data → Validation → Processing → ML Model → Results
```

### 3. **Error Handling**
```
try:
    # All processing
except Exception as e:
    # Return error page
```

### 4. **Separation of Concerns**
- routes.py: Request handling
- prediction.py: ML predictions
- recommendation.py: Recommendations
- utils.py: Utilities

### 5. **Pre-trained Models**
- Loaded once at startup
- Reused for all predictions
- Faster than retraining

---

## 💡 Why This Architecture?

✅ **Modular**: Each file has specific responsibility
✅ **Scalable**: Easy to add new features
✅ **Maintainable**: Clear code organization
✅ **Testable**: Each module can be tested independently
✅ **Efficient**: Models loaded once, reused
✅ **Robust**: Error handling throughout

---

**This is a production-ready backend architecture! 🎓**
