# SmartHome Finder - Capstone Project Documentation

## 📋 Project Overview

**SmartHome Finder** is an intelligent property recommendation system that uses machine learning to help users find their ideal residential property. It combines price prediction with smart property matching based on user preferences and accessibility scores.

---

## 🎯 Project Goals

1. **Price Prediction**: Predict property prices based on features like BHK, area, amenities, etc.
2. **Smart Recommendations**: Suggest properties that match user preferences
3. **Affordability Analysis**: Determine if properties fit within user budget
4. **Accessibility Scoring**: Evaluate proximity to metro stations and hospitals
5. **User-Friendly Interface**: Web-based UI for easy property search

---

## 🏗️ Architecture Overview

### Tech Stack
- **Backend**: Python Flask (Web Framework)
- **Frontend**: HTML, CSS, JavaScript (Jinja2 Templates)
- **ML/Data**: scikit-learn, pandas, numpy
- **Mapping**: Leaflet.js (Interactive maps)
- **Data**: CSV dataset with property information

### Project Structure
```
HomeFinder/
├── main.py                          # Entry point
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── routes.py                   # API endpoints
│   ├── prediction.py               # ML price prediction
│   ├── recommendation.py           # Property recommendation engine
│   └── utils.py                    # Utility functions (accessibility)
├── models/
│   ├── model.pkl                   # Trained ML model (Random Forest)
│   ├── scaler.pkl                  # Feature scaler
│   └── features.pkl                # Feature names
├── data/
│   └── combined_final_dataset.csv  # Property dataset
├── templates/
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   └── results.html                # Results page
├── static/
│   └── style.css                   # Styling
└── requirements.txt                # Dependencies

```

---

## 🔄 How It Works - Step by Step

### 1. **User Input Phase** (index.html)
User provides:
- **City**: Delhi, Mumbai, or Bangalore
- **BHK**: Number of bedrooms
- **Bathrooms**: Number of bathrooms
- **Balconies**: Number of balconies
- **Area**: Carpet area in sqft
- **Property Age**: Age in years
- **Amenities**: Number of amenities
- **Budget**: Budget in lakhs (₹)
- **Location**: Click on map to select coordinates

### 2. **Data Processing** (routes.py - /predict endpoint)
```
User Input → Validation → City Coordinates → Accessibility Score
```

**Key Processing Steps:**
- Validates all numeric inputs
- Converts budget from lakhs to INR
- Gets city center coordinates from dataset
- Calculates accessibility score for that location

### 3. **Price Prediction** (prediction.py)
```
User Features → Feature Alignment → Scaling → ML Model → Price Prediction
```

**Process:**
- Converts user input to DataFrame
- Aligns features with trained model features
- Scales features using pre-trained scaler
- Random Forest model predicts price
- Calculates confidence interval (lower/upper bounds)

**Output:**
```python
{
    "predicted_price": 5000000,      # Predicted price in INR
    "lower": 4800000,                # Lower bound
    "upper": 5200000                 # Upper bound
}
```

### 4. **Property Recommendation** (recommendation.py)
This is the core intelligence of the system.

**Step 1: Filtering**
- Filter properties by city
- Filter by area (±20% of user area)
- Filter by BHK (±1 from user BHK)
- Filter by budget (≤120% of user budget)
- Fallback: If <10 results, show all city properties

**Step 2: Feature Weighting**
Assign importance weights to features:
- BHK: Weight 3 (most important)
- Area: Weight 3 (most important)
- Bathrooms: Weight 2
- Accessibility: Weight 2
- Other features: Weight 1

**Step 3: Similarity Scoring**
- Use Cosine Similarity to compare user preferences with properties
- Weighted features for better matching
- Top 15 candidates selected

**Step 4: Scoring Algorithm**
Calculate multiple scores:

```
Similarity Score = Cosine similarity between user and property
Affordability Score = Budget / Property Price
Accessibility Score = 1 / (1 + avg_distance_to_landmarks)
BHK Bonus = +10 if BHK matches exactly

Final Score = 
    0.5 × (Similarity × 100) +
    0.3 × (Affordability × 100) +
    0.2 × (Accessibility × 100) +
    BHK Bonus

Match Percent = Normalize Final Score to 0-100%
```

**Step 5: Ranking & Output**
- Sort by Final Score (descending)
- Return top 5 properties
- Include all relevant details

### 5. **Accessibility Calculation** (utils.py)
```
Property Location → Distance to Landmarks → Accessibility Score
```

**Landmarks by City:**
- **Delhi**: Metro stations, hospitals
- **Mumbai**: Metro stations, hospitals
- **Bangalore**: Metro stations, hospitals

**Formula:**
```
Min distances to each landmark category
Average distance = (min_metro_dist + min_hospital_dist) / 2
Accessibility Score = 1 / (1 + avg_distance)
Range: 0 to 1 (higher = better)
```

### 6. **Results Display** (results.html)
Shows:
- **Predicted Price**: With confidence range
- **Affordability Label**: Affordable/Slightly Expensive/Expensive
- **Property Cards**: Top 5 recommendations with:
  - Match percentage
  - Price
  - Area
  - Amenities
  - Accessibility rating
  - RERA status
- **Sorting Options**: By Match %, Area, Price, Affordability
- **Modal Details**: Click "View Details" to see full property info on map

---

## 📊 Key Features Explained

### 1. **Hybrid Scoring System**
Combines three factors:
- **Similarity (50%)**: How well property matches user preferences
- **Affordability (30%)**: Budget fit
- **Accessibility (20%)**: Proximity to important locations

### 2. **Error Handling**
- Input validation with try-except blocks
- Default values for missing inputs
- Graceful fallbacks (e.g., Delhi coordinates if city not found)
- Division by zero protection

### 3. **Responsive UI**
- Interactive Leaflet maps
- Modal popups for property details
- Sorting and filtering options
- Mobile-friendly design

### 4. **Machine Learning Integration**
- Pre-trained Random Forest model
- Feature scaling for normalization
- Confidence intervals for predictions
- Weighted feature importance

---

## 🔧 Technical Details

### Machine Learning Model
- **Type**: Random Forest Regressor
- **Input Features**: BHK, Bathrooms, Area, Age, Amenities, Accessibility, etc.
- **Output**: Property price in INR
- **Confidence**: Calculated from individual tree predictions

### Data Flow
```
CSV Dataset → Pandas DataFrame → Feature Engineering → 
ML Model Training → Model Serialization (pickle) → 
Prediction on New Data
```

### Similarity Calculation
Uses **Cosine Similarity**:
- Measures angle between user preference vector and property vector
- Range: -1 to 1 (1 = perfect match)
- Weighted by feature importance

---

## 💡 Key Algorithms

### 1. Cosine Similarity
```
similarity = (A · B) / (||A|| × ||B||)
Where A = user preferences, B = property features
```

### 2. Accessibility Score
```
score = 1 / (1 + average_distance_km)
Higher distance → Lower score
```

### 3. Affordability Score
```
score = user_budget / property_price
score ≥ 1.0 → Affordable
0.8 ≤ score < 1.0 → Slightly Expensive
score < 0.8 → Expensive
```

---

## 🎓 Learning Outcomes

This project demonstrates:

1. **Full-Stack Development**
   - Backend: Flask, Python
   - Frontend: HTML, CSS, JavaScript
   - Database: CSV data handling

2. **Machine Learning**
   - Model training and serialization
   - Feature scaling and normalization
   - Prediction with confidence intervals

3. **Data Science**
   - Data filtering and aggregation
   - Feature engineering
   - Similarity metrics

4. **Software Engineering**
   - Error handling and validation
   - Code organization (MVC pattern)
   - API design (REST endpoints)

5. **Web Development**
   - Template rendering (Jinja2)
   - Interactive UI (JavaScript)
   - Geolocation and mapping (Leaflet)

---

## 🚀 How to Use

1. **Start the server**: `python main.py`
2. **Open browser**: `http://localhost:5000`
3. **Fill the form**:
   - Select city
   - Enter property preferences
   - Click on map to select location
   - Enter budget
4. **View results**:
   - See predicted price
   - Browse recommended properties
   - Sort by different criteria
   - Click "View Details" for more info

---

## 📈 Potential Enhancements

1. **Database Integration**: Replace CSV with PostgreSQL/MongoDB
2. **User Accounts**: Save favorite properties
3. **Advanced Filters**: Price range, furnishing type, etc.
4. **Real-time Data**: Integrate with property APIs
5. **Mobile App**: React Native/Flutter version
6. **Notifications**: Alert users about new properties
7. **Reviews & Ratings**: User feedback system
8. **Virtual Tours**: 3D property visualization

---

## 🔐 Security Considerations

- Input validation on all forms
- Error messages don't expose system details
- No sensitive data in logs
- CSRF protection (can be added)
- SQL injection prevention (using pandas, not raw SQL)

---

## 📝 Summary

SmartHome Finder is a **complete end-to-end machine learning application** that:
- ✅ Predicts property prices accurately
- ✅ Recommends properties intelligently
- ✅ Provides accessibility insights
- ✅ Offers user-friendly interface
- ✅ Handles errors gracefully
- ✅ Demonstrates full-stack development skills

This project is perfect for a capstone as it combines **ML, web development, data science, and software engineering** in a practical, real-world application.

---

## 🎯 Capstone Project Highlights

**What makes this a strong capstone:**

1. **Complexity**: Multi-component system with ML, web, and data layers
2. **Real-world Application**: Solves actual problem (property search)
3. **Technical Depth**: ML models, algorithms, web frameworks
4. **User Experience**: Interactive UI with maps and filtering
5. **Error Handling**: Robust and production-ready
6. **Scalability**: Can be extended with more features
7. **Documentation**: Well-commented and organized code

---

**Good luck with your capstone presentation! 🎓**
