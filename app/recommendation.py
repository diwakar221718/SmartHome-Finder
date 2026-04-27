import joblib
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.utils import calculate_accessibility

# ----------------------------
# Load artifacts
# ----------------------------
scaler = joblib.load('models/scaler.pkl')
features = joblib.load('models/features.pkl')

# ----------------------------
# Load dataset
# ----------------------------
df = pd.read_csv('data/combined_final_dataset.csv')


def recommend_properties(user_input, budget, top_n=5):

    # ----------------------------
    # Ensure column exists
    # ----------------------------
    if 'AccessibilityScore' not in df.columns:
        df['AccessibilityScore'] = 0.5

    # ----------------------------
    # USER INPUT
    # ----------------------------
    user_area = user_input.get("CarpetArea_sqft", 0)
    user_bhk = user_input.get("BHK", 0)
    user_city = user_input.get("City")

    # ----------------------------
    # FILTERS
    # ----------------------------
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

    # fallback
    if len(df_filtered) < 10:
        df_filtered = df[df["City"] == user_city]

    # ----------------------------
    # MODEL INPUT
    # ----------------------------
    data = df_filtered[features]

    user_df = pd.DataFrame([user_input])
    user_df = user_df.reindex(columns=features, fill_value=0)

    # ----------------------------
    # SCALE
    # ----------------------------
    data_scaled = scaler.transform(data)
    user_scaled = scaler.transform(user_df)

    # ----------------------------
    # FEATURE WEIGHTS
    # ----------------------------
    weights = np.ones(len(features))

    for i, f in enumerate(features):
        if f == "BHK":
            weights[i] = 3
        elif "Area" in f:
            weights[i] = 3
        elif f == "Bathrooms":
            weights[i] = 2
        elif f == "AccessibilityScore":
            weights[i] = 2

    data_scaled *= weights
    user_scaled *= weights

    # ----------------------------
    # SIMILARITY
    # ----------------------------
    sim = cosine_similarity(user_scaled, data_scaled)[0]

    scores = sorted(list(enumerate(sim)), key=lambda x: x[1], reverse=True)

    # take more for better ranking
    top = scores[:15]

    indices = [i[0] for i in top]
    raw_scores = [i[1] for i in top]

    # ----------------------------
    # RESULT DATA
    # ----------------------------
    result = df_filtered.iloc[indices].copy()
    
    # Handle empty results
    if len(result) == 0:
        return []

    # ----------------------------
    # ACCESSIBILITY
    # ----------------------------
    result['AccessibilityScore'] = result.apply(
        lambda row: calculate_accessibility(
            row['City'], row['Latitude'], row['Longitude']
        ),
        axis=1
    )

    # ----------------------------
    # INITIAL MATCH (raw similarity)
    # ----------------------------
    result['SimilarityScore'] = raw_scores

    # ----------------------------
    # AFFORDABILITY
    # ----------------------------
    result['AffordabilityScore'] = result['Price_INR'].apply(
        lambda x: budget / x if x > 0 else 0
    )

    def label(x):
        if x >= 1:
            return "Affordable ✅"
        elif x >= 0.8:
            return "Slightly Expensive ⚠️"
        else:
            return "Expensive ❌"

    result['AffordabilityLabel'] = result['AffordabilityScore'].apply(label)

    # ----------------------------
    # BHK BONUS
    # ----------------------------
    result['BHK_Bonus'] = result['BHK'].apply(
        lambda x: 10 if x == user_bhk else 0
    )

    # ----------------------------
    # FINAL HYBRID SCORE
    # ----------------------------
    result['FinalScore'] = (
        0.5 * (result['SimilarityScore'] * 100) +
        0.3 * (result['AffordabilityScore'] * 100) +
        0.2 * (result['AccessibilityScore'] * 100)
    )

    result['FinalScore'] += result['BHK_Bonus']

    # ----------------------------
    # NORMALIZE FINAL SCORE → %
    # ----------------------------
    min_fs = result['FinalScore'].min()
    max_fs = result['FinalScore'].max()

    result['MatchPercent'] = result['FinalScore'].apply(
        lambda x: round((x - min_fs) / (max_fs - min_fs + 1e-5) * 100)
    )

    # ----------------------------
    # FINAL SORT
    # ----------------------------
    result = result.sort_values(by='FinalScore', ascending=False)

    # ----------------------------
    # TOP N
    # ----------------------------
    result = result.head(top_n)

    # ----------------------------
    # OUTPUT
    # ----------------------------
    result = result.reindex(columns=[
    'BHK',
    'Bathrooms',
    'Balconies',
    'CarpetArea_sqft',
    'BuiltUpArea_sqft',
    'SuperBuiltUpArea_sqft',
    'Floor',
    'TotalFloors',
    'Furnishing',
    'Parking',
    'BuildingType',
    'Facing',
    'AmenitiesCount',
    'Price_INR',
    'Latitude',
    'Longitude',
    'AccessibilityScore',
    'MatchPercent',
    'AffordabilityLabel',
    'IsRERARegistered'
], fill_value="N/A")

    return result.to_dict(orient='records')