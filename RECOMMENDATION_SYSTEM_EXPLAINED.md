# Recommendation System Explained

## 🎯 Type of Recommendation System Used

Your SmartHome Finder uses a **HYBRID RECOMMENDATION SYSTEM** that combines multiple approaches:

1. **Content-Based Filtering** (Primary)
2. **Similarity Matching** (Cosine Similarity)
3. **Scoring Algorithm** (Multi-factor ranking)

---

## 📊 System Architecture

```
User Input
    ↓
[Content-Based Filtering]
    ↓
Filter by: City, Area, BHK, Budget
    ↓
[Similarity Matching]
    ↓
Calculate Cosine Similarity between user & properties
    ↓
[Multi-Factor Scoring]
    ↓
Score = Similarity (50%) + Affordability (30%) + Accessibility (20%)
    ↓
[Ranking & Output]
    ↓
Return Top 5 Properties
```

---

## 1️⃣ CONTENT-BASED FILTERING

### What is it?
Recommends properties based on **features/attributes** that match user preferences.

### How it works in your project:

**Step 1: Filter by City**
```python
df_filtered = df[df["City"] == user_city]
# Only show properties in the selected city
```

**Step 2: Filter by Area (±20%)**
```python
df_filtered = df_filtered[
    (df_filtered["CarpetArea_sqft"] >= 0.8 * user_area) &
    (df_filtered["CarpetArea_sqft"] <= 1.2 * user_area)
]
# If user wants 1000 sqft, show 800-1200 sqft properties
```

**Step 3: Filter by BHK (±1)**
```python
df_filtered = df_filtered[
    df_filtered["BHK"].between(user_bhk - 1, user_bhk + 1)
]
# If user wants 2 BHK, show 1-3 BHK properties
```

**Step 4: Filter by Budget (≤120%)**
```python
df_filtered = df_filtered[
    df_filtered["Price_INR"] <= 1.2 * budget
]
# If user budget is ₹50 lakhs, show properties up to ₹60 lakhs
```

### Example:
```
User Input:
- City: Delhi
- Area: 1200 sqft
- BHK: 2
- Budget: ₹50 lakhs

Content-Based Filtering Result:
- Delhi properties only ✓
- 960-1440 sqft ✓
- 1-3 BHK ✓
- ≤ ₹60 lakhs ✓

Filtered Results: 50 properties (from 1000 total)
```

### Advantages:
✅ Fast filtering
✅ Removes irrelevant properties
✅ Reduces search space
✅ User-specific results

### Disadvantages:
❌ May miss good properties outside ranges
❌ Rigid filtering rules
❌ Doesn't consider quality/popularity

---

## 2️⃣ SIMILARITY-BASED MATCHING (Cosine Similarity)

### What is it?
Measures **how similar** each property is to user preferences using mathematical similarity.

### How it works:

**Step 1: Feature Weighting**
```python
weights = {
    "BHK": 3,                    # Most important
    "CarpetArea_sqft": 3,        # Most important
    "Bathrooms": 2,              # Important
    "AccessibilityScore": 2,     # Important
    "Other features": 1          # Less important
}
```

**Step 2: Create Vectors**
```
User Vector:     [2, 1200, 2, 0.7, 8, ...]
Property 1:      [2, 1150, 2, 0.65, 8, ...]
Property 2:      [3, 1500, 3, 0.5, 10, ...]
Property 3:      [2, 1200, 2, 0.7, 8, ...]
```

**Step 3: Apply Weights**
```
User Vector (weighted):     [6, 3600, 4, 1.4, 8, ...]
Property 1 (weighted):      [6, 3450, 4, 1.3, 8, ...]
Property 2 (weighted):      [9, 4500, 6, 1.0, 10, ...]
Property 3 (weighted):      [6, 3600, 4, 1.4, 8, ...]
```

**Step 4: Calculate Cosine Similarity**
```
Cosine Similarity = (A · B) / (||A|| × ||B||)

Property 1 similarity: 0.98 (Very similar!)
Property 2 similarity: 0.75 (Somewhat similar)
Property 3 similarity: 1.00 (Perfect match!)
```

### Formula Visualization:
```
        User Preference Vector
                 ↗
                /  θ (angle)
               /
              / ← Smaller angle = Higher similarity
             /
            ↙
    Property Vector

Cosine Similarity = cos(θ)
- θ = 0° → similarity = 1.0 (Perfect match)
- θ = 90° → similarity = 0.0 (No match)
- θ = 180° → similarity = -1.0 (Opposite)
```

### Example:
```
User wants: 2 BHK, 1200 sqft, 2 bathrooms, accessible location

Property A: 2 BHK, 1150 sqft, 2 bathrooms, accessible
Similarity: 0.98 ⭐⭐⭐⭐⭐ (Excellent match!)

Property B: 3 BHK, 1500 sqft, 3 bathrooms, less accessible
Similarity: 0.75 ⭐⭐⭐ (Good match)

Property C: 1 BHK, 800 sqft, 1 bathroom, not accessible
Similarity: 0.45 ⭐⭐ (Poor match)
```

### Advantages:
✅ Considers all features together
✅ Finds best matches mathematically
✅ Flexible (not rigid like filtering)
✅ Handles partial matches well

### Disadvantages:
❌ Computationally expensive for large datasets
❌ Requires feature scaling
❌ Sensitive to feature weights

---

## 3️⃣ MULTI-FACTOR SCORING ALGORITHM

### What is it?
Combines **multiple scoring factors** to rank properties comprehensively.

### The Three Factors:

#### Factor 1: Similarity Score (50% weight)
```
Similarity Score = Cosine Similarity × 100
Range: 0-100

How well does the property match user preferences?
```

#### Factor 2: Affordability Score (30% weight)
```
Affordability Score = (User Budget / Property Price) × 100
Range: 0-200+

Can user afford this property?
- Score ≥ 100 → Affordable (within budget)
- Score 80-100 → Slightly expensive (10-20% over budget)
- Score < 80 → Expensive (>20% over budget)
```

#### Factor 3: Accessibility Score (20% weight)
```
Accessibility Score = 1 / (1 + average_distance_to_landmarks) × 100
Range: 0-100

How close is the property to important locations?
- Score > 70 → Good accessibility (close to metro/hospital)
- Score 40-70 → Moderate accessibility
- Score < 40 → Poor accessibility (far from landmarks)
```

### Final Score Calculation:
```python
Final Score = (
    0.5 × Similarity_Score +
    0.3 × Affordability_Score +
    0.2 × Accessibility_Score
) + BHK_Bonus

BHK_Bonus = +10 if property BHK matches user BHK exactly
```

### Example Calculation:

```
User: 2 BHK, 1200 sqft, ₹50 lakhs budget, wants accessible location

Property A:
- Similarity Score: 95 (very similar)
- Affordability Score: 110 (affordable, within budget)
- Accessibility Score: 80 (good accessibility)
- BHK Match: Yes (+10 bonus)

Final Score = (0.5 × 95) + (0.3 × 110) + (0.2 × 80) + 10
            = 47.5 + 33 + 16 + 10
            = 106.5

Match Percent = 85% ⭐⭐⭐⭐⭐


Property B:
- Similarity Score: 70 (somewhat similar)
- Affordability Score: 90 (slightly expensive)
- Accessibility Score: 50 (moderate accessibility)
- BHK Match: No (0 bonus)

Final Score = (0.5 × 70) + (0.3 × 90) + (0.2 × 50) + 0
            = 35 + 27 + 10 + 0
            = 72

Match Percent = 58% ⭐⭐⭐
```

### Ranking:
```
Rank 1: Property A (106.5 score) - 85% match
Rank 2: Property B (72 score) - 58% match
Rank 3: Property C (65 score) - 52% match
...
```

---

## 🔄 Complete Recommendation Flow

```
1. USER INPUT
   ↓
   City: Delhi, BHK: 2, Area: 1200 sqft, Budget: ₹50L, Amenities: 8

2. CONTENT-BASED FILTERING
   ↓
   Filter by: City, Area (±20%), BHK (±1), Budget (≤120%)
   Result: 50 properties (from 1000)

3. SIMILARITY MATCHING
   ↓
   Calculate cosine similarity for all 50 properties
   Select top 15 most similar properties

4. MULTI-FACTOR SCORING
   ↓
   Calculate: Similarity (50%) + Affordability (30%) + Accessibility (20%)
   Add BHK bonus if applicable

5. RANKING
   ↓
   Sort by Final Score (descending)
   Select top 5 properties

6. OUTPUT
   ↓
   Display top 5 recommendations with:
   - Match percentage
   - Price prediction
   - Affordability label
   - Accessibility rating
   - All property details
```

---

## 📈 Why This Hybrid Approach?

### Content-Based Filtering
- **Fast**: Quickly eliminates irrelevant properties
- **Precise**: Ensures basic requirements are met

### Similarity Matching
- **Intelligent**: Finds best matches mathematically
- **Flexible**: Handles partial matches

### Multi-Factor Scoring
- **Comprehensive**: Considers multiple perspectives
- **Balanced**: Weights different factors appropriately
- **User-Centric**: Prioritizes what matters most

### Combined Benefits:
✅ Fast (filtering reduces search space)
✅ Accurate (similarity finds best matches)
✅ Comprehensive (multiple factors considered)
✅ Balanced (weighted scoring)
✅ Scalable (works with large datasets)

---

## 🎓 Comparison with Other Systems

### Collaborative Filtering
```
❌ Not used in your project
Why? Requires user ratings/history
Your project: First-time users, no history available
```

### Content-Based Only
```
⚠️ Partially used (filtering step)
Limitation: Too rigid, misses good properties
Your project: Enhanced with similarity matching
```

### Hybrid (Your Project)
```
✅ Best approach!
Combines: Filtering + Similarity + Multi-factor scoring
Result: Fast, accurate, comprehensive recommendations
```

---

## 💡 Key Takeaways

1. **Your system is HYBRID** - combines multiple techniques
2. **Content-Based Filtering** - Fast initial filtering
3. **Cosine Similarity** - Intelligent matching
4. **Multi-Factor Scoring** - Comprehensive ranking
5. **Weighted Factors** - Similarity (50%), Affordability (30%), Accessibility (20%)
6. **Top-N Recommendation** - Returns top 5 properties

---

## 🚀 For Your Capstone Presentation

**You can say:**

> "Our SmartHome Finder uses a **hybrid recommendation system** that combines:
> 1. **Content-based filtering** for fast initial screening
> 2. **Cosine similarity matching** for intelligent property matching
> 3. **Multi-factor scoring algorithm** that weighs similarity (50%), affordability (30%), and accessibility (20%)
> 
> This approach ensures we recommend properties that are not just similar to user preferences, but also affordable and accessible, providing a comprehensive and balanced recommendation."

---

**This is a sophisticated recommendation system perfect for a capstone project! 🎓**
