import joblib
import numpy as np
import pandas as pd

model = joblib.load('models/model.pkl')
scaler = joblib.load('models/scaler.pkl')
features = joblib.load('models/features.pkl')


def predict_price(user_input):

    # ✅ Convert to DataFrame (preserves feature names)
    input_df = pd.DataFrame([user_input])

    # align columns
    input_df = input_df.reindex(columns=features, fill_value=0)

    # scale
    input_scaled = scaler.transform(input_df)

    # prediction
    pred = model.predict(input_scaled)[0]

    # confidence interval
    tree_preds = [tree.predict(input_scaled)[0] for tree in model.estimators_]

    mean = np.mean(tree_preds)
    std = np.std(tree_preds)

    return {
        "predicted_price": round(pred),
        "lower": round(mean - std),
        "upper": round(mean + std)
    }