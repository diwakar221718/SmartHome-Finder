# SmartHome Finder 🏠

An intelligent property recommendation system using Machine Learning and Flask.

## Features

- 🤖 **ML Price Prediction** - Predicts property prices using Random Forest
- 🎯 **Smart Recommendations** - Hybrid recommendation system with similarity matching
- 💰 **Affordability Analysis** - Determines if properties fit your budget
- 📍 **Accessibility Scoring** - Evaluates proximity to metro stations and hospitals
- 🗺️ **Interactive Maps** - Leaflet.js for property location visualization

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **ML**: scikit-learn, pandas, numpy
- **Mapping**: Leaflet.js

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/diwakar221718/SmartHome-Finder.git
cd SmartHome-Finder
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

5. **Open in browser**
```
http://localhost:5000
```

## How It Works

### Step 1: User Input
- Select city (Delhi, Mumbai, Bangalore)
- Enter property preferences (BHK, bathrooms, area, budget)
- Click on map to select location

### Step 2: Price Prediction
- ML model predicts property price
- Shows confidence interval (lower/upper bounds)

### Step 3: Get Recommendations
- Filters properties by city, area, BHK, budget
- Calculates similarity using cosine similarity
- Scores using: Similarity (50%) + Affordability (30%) + Accessibility (20%)
- Returns top 5 recommendations

### Step 4: View Results
- See predicted price
- Browse recommended properties
- Sort by match %, area, price, or affordability
- Click "View Details" to see property on map

## Recommendation Algorithm

**Type**: Hybrid Recommendation System

**Process**:
1. **Content-Based Filtering** - Filters by city, area, BHK, budget
2. **Similarity Matching** - Cosine similarity with weighted features
3. **Multi-Factor Scoring** - Combines three factors:
   - Similarity Score (50%)
   - Affordability Score (30%)
   - Accessibility Score (20%)

## Machine Learning Model

- **Algorithm**: Random Forest Regressor
- **Input Features**: BHK, Bathrooms, Area, Age, Amenities, Accessibility
- **Output**: Property price in INR
- **Confidence**: Calculated from individual tree predictions

## Project Structure

```
SmartHome-Finder/
├── main.py                    # Entry point
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── routes.py             # API endpoints
│   ├── prediction.py         # ML price prediction
│   ├── recommendation.py     # Recommendation engine
│   └── utils.py              # Utility functions
├── models/
│   ├── model.pkl             # Trained ML model
│   ├── scaler.pkl            # Feature scaler
│   └── features.pkl          # Feature names
├── data/
│   └── combined_final_dataset.csv
├── templates/
│   ├── base.html
│   ├── index.html
│   └── results.html
├── static/
│   └── style.css
└── requirements.txt
```

## Usage Example

1. Visit http://localhost:5000
2. Select "Delhi" as city
3. Enter: 2 BHK, 2 bathrooms, 1200 sqft, ₹50 lakhs budget
4. Click on map to select location
5. Click "Find Properties"
6. View predicted price and recommendations
7. Sort and explore properties

## License

MIT License - see LICENSE file for details

## Author

**Diwakar Yadav**
