import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def load_data(filepath):
    df = pd.read_csv(filepath)
    X = df[['score', 'stars']]
    y = df['price_2_adultsnight']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model

def train_gradient_boosting(X_train, y_train):
    model = GradientBoostingRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model

def train_svr(X_train, y_train):
    model = SVR()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'MSE: {mse}')
    print(f'R2: {r2}')
    return mse, r2

def save_model(model, filename):
    joblib.dump(model, filename)

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = load_data('EDA/cleaned_bookings.csv')

    print("Linear Regression:")
    linear_model = train_linear_regression(X_train, y_train)
    evaluate_model(linear_model, X_test, y_test)
    save_model(linear_model, 'price_linear.joblib')

    print("\nRandom Forest Regression:")
    rf_model = train_random_forest(X_train, y_train)
    evaluate_model(rf_model, X_test, y_test)
    save_model(rf_model, 'price_randomforest.joblib')

    print("\nGradient Boosting Regression:")
    gb_model = train_gradient_boosting(X_train, y_train)
    evaluate_model(gb_model, X_test, y_test)
    save_model(gb_model, 'price_gradientboost.joblib')

    print("\nSupport Vector Regression:")
    svr_model = train_svr(X_train, y_train)
    evaluate_model(svr_model, X_test, y_test)
    save_model(svr_model, 'price_supportvector.joblib')
