import joblib
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#model_name = input("Enter model name (linear, gradientboost, randomforest, supportvector): ")
score = float(input("Enter hotel score (e.g., 8.5): "))
stars = int(input("Enter hotel stars (e.g., 4): "))
model_name = ['linear', 'gradientboost', 'randomforest', 'supportvector']
for i in range(len(model_name)):
    model = joblib.load(f'ML Train\price_{model_name[i]}.joblib')
    predicted_price = round(model.predict(np.array([[score, stars]]))[0])
    print(f'Predicted price of {model_name[i]}: VND {predicted_price}')