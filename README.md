# 🏠 SmartHome Finder - Intelligent Property Recommendation System

A machine learning-powered web application that helps users find their ideal residential property by predicting prices and recommending properties based on user preferences, affordability, and accessibility.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
- [Machine Learning Model](#machine-learning-model)
- [Recommendation System](#recommendation-system)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### 🎯 Core Features
- **Price Prediction**: ML-powered price prediction with confidence intervals
- **Smart Recommendations**: Hybrid recommendation system combining content-based filtering and similarity matching
- **Affordability Analysis**: Determines if properties fit within user budget
- **Accessibility Scoring**: Evaluates proximity to metro stations and hospitals
- **Interactive Maps**: Leaflet.js integration for location selection and property viewing
- **Multi-factor Ranking**: Scores properties based on similarity (50%), affordability (30%), and accessibility (20%)

### 🔍 Search Capabilities
- Filter by city (Delhi, Mumbai, Bangalore)
- Filter by BHK, bathrooms, balconies
- Filter by carpet area and property age
- Filter by amenities count
- Set budget in lakhs (₹)
- Sort results by match %, area, price, or affordability

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Machine Learning**: scikit-learn (Random Forest)
- **Data Processing**: pandas, numpy
- **Geolocation**: geopy

### Frontend
- **HTML/CSS/JavaScript**: Jinja2 templating
- **Maps**: Leaflet.js
- **Styling**: Custom CSS

### Data & Models
- **Dataset**: CSV with property information
- **ML Model**: Random Forest Regressor
- **Model Serialization**: joblib (pickle)

---

## 📁 Project Structure

```
SmartHome-Finder/
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
│
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── routes.py                   # API endpoints
│   ├── prediction.py               # ML price prediction
│   ├── recommendation.py           # Recommendation engine
│   └── utils.py                    # Utility functions
│
├── models/
│   ├── model.pkl                   # Trained Random Forest model
│   ├── scaler.pkl                  # Feature scaler
│   └── features.pkl                # Feature names
│
├── data/
│   └── combined_final_dataset.csv  # Property dataset
│
├── templates/
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   └── results.html                # Results page
│
└── static/
    └── style.css                   # Styling
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/SmartHome-Finder.git
cd SmartHome-Finder
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python main.py
```

### Step 5: Open in Browser
```
http://localhost:5000
```

---

## 💻 Usage

### 1. **Home Page**
- Select a city (Delhi, Mumbai, or Bangalore)
- Enter property preferences:
  - BHK (number of bedrooms)
  - Bathrooms
  - Balconies
  - Carpet area (sqft)
  - Property age (years)
  - Amenities count
  - Budget (in lakhs)
- Click on map to select location
- Click "Find Properties"

### 2. **Results Page**
- View predicted price with confidence range
- Browse top 5 recommended properties
- See match percentage for each property
- Check affordability status
- View accessibility rating
- Sort results by:
  - Match %
  - Area
  - Price
  - Affordability
- Click "View Details" to see property on map

---

## 🔄 How It Works

### Request Flow
```
User Input (Form)
    ↓
Validation & Processing
    ↓
City Coordinates Extraction
    ↓
Accessibility Score Calculation
    ↓
ML Price Prediction
    ↓
Property Recommendation Engine
    ↓
Multi-factor Scoring & Ranking
    ↓
Results Display
```

### Price Prediction
1. User input converted to feature vector
2. Features scaled using pre-trained scaler
3. Random Forest model predicts price
4. Confidence interval calculated from tree predictions

### Recommendation Algorithm
1. **Content-Based Filtering**: Filter by city, area (±20%), BHK (±1), budget
2. **Similarity Matching**: Cosine similarity with weighted features
3. **Multi-Factor Scoring**: 
   - Similarity (50%)
   - Affordability (30%)
   - Accessibility (20%)
4. **Ranking**: Sort by final score, return top 5

---

## 🔌 API Endpoints

### GET /
**Description**: Home page with search form
**Response**: HTML page with city dropdown and search form

### POST /predict
**Description**: Predict price and get recommendations
**Request Body**:
```json
{
  "city": "Delhi",
  "bhk": 2,
  "bathrooms": 2,
  "balconies": 1,
  "area": 1200,
  "age": 5,
  "amenities": 8,
  "budget": 50,
  "sort": "match"
}
```
**Response**: HTML page with results

---

## 🤖 Machine Learning Model

### Model Type
- **Algorithm**: Random Forest Regressor
- **Trees**: 100
- **Features**: 15+ property features

### Features Used
- BHK (bedrooms)
- Bathrooms
- Balconies
- Carpet Area (sqft)
- Built-up Area (sqft)
- Super Built-up Area (sqft)
- Floor number
- Total floors
- Furnishing type
- Parking spaces
- Building type
- Facing direction
- Amenities count
- Latitude
- Longitude
- Accessibility score

### Model Performance
- Provides price predictions with confidence intervals
- Calculates uncertainty from tree predictions
- Robust to outliers and non-linear relationships

---

## 🎯 Recommendation System

### Type: Hybrid Recommendation System

**Components:**
1. **Content-Based Filtering**
   - Filters by city, area, BHK, budget
   - Fast initial screening

2. **Similarity Matching**
   - Cosine similarity calculation
   - Weighted feature importance
   - BHK & Area: Weight 3
   - Bathrooms & Accessibility: Weight 2

3. **Multi-Factor Scoring**
   - Similarity Score (50%): How well property matches preferences
   - Affordability Score (30%): Budget fit
   - Accessibility Score (20%): Proximity to landmarks
   - BHK Bonus: +10 if exact match

### Accessibility Calculation
- Distance to nearest metro station
- Distance to nearest hospital
- Formula: `1 / (1 + average_distance_km)`
- Range: 0-1 (higher = better)

---

## 📊 Sample Output

### Predicted Price
```
Predicted Price: ₹50,00,000
Range: ₹48,00,000 - ₹52,00,000
Affordability: Affordable ✅
```

### Recommended Property
```
BHK: 2
Area: 1150 sqft
Price: ₹49,00,000
Match: 85%
Affordability: Affordable ✅
Accessibility: Good 🟢
RERA: Approved ✅
```

---

## 🔧 Configuration

### Environment Variables
Create `.env` file (optional):
```
FLASK_ENV=development
FLASK_DEBUG=True
```

### Flask Configuration
Edit `app/__init__.py` to modify:
- Template folder path
- Static folder path
- Debug mode

---

## 📝 Dependencies

See `requirements.txt` for complete list:
- Flask==3.1.3
- pandas==3.0.2
- numpy==2.4.4
- scikit-learn==1.8.0
- joblib==1.5.3
- geopy==2.4.1
- Jinja2==3.1.6

---

## 🐛 Troubleshooting

### Issue: Templates not found
**Solution**: Ensure `templates/` folder exists in project root

### Issue: Models not found
**Solution**: Ensure `models/` folder with `.pkl` files exists

### Issue: Dataset not found
**Solution**: Ensure `data/combined_final_dataset.csv` exists

### Issue: Port 5000 already in use
**Solution**: Change port in `main.py`:
```python
app.run(debug=True, port=5001)
```

---

## 🚀 Deployment

### Deploy to Heroku
1. Create `Procfile`:
```
web: gunicorn main:app
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Deploy to AWS/GCP
- Use Flask with gunicorn
- Configure environment variables
- Set up database (optional)

---

## 📚 Documentation

- `PROJECT_DOCUMENTATION.md` - Complete project overview
- `BACKEND_EXPLANATION.md` - Backend architecture details
- `RECOMMENDATION_SYSTEM_EXPLAINED.md` - Recommendation algorithm details
- `FLASK_EXPLANATION.md` - Flask framework explanation

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 Author

**Diwakar Yadav**
- Capstone Project
- SmartHome Finder - Intelligent Property Recommendation System

---

## 🙏 Acknowledgments

- Flask documentation and community
- scikit-learn for ML algorithms
- Leaflet.js for mapping
- geopy for geolocation services

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

## 🎓 Capstone Project

This project demonstrates:
- ✅ Full-stack web development
- ✅ Machine learning integration
- ✅ Data science and analytics
- ✅ Software engineering best practices
- ✅ User-friendly interface design
- ✅ Error handling and validation
- ✅ Code organization and modularity

**Status**: Complete and Production-Ready ✅

---

**Last Updated**: April 2026
**Version**: 1.0.0
