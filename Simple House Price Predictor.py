import numpy as np
from sklearn.linear_model import LinearRegression

def train_price_model() -> LinearRegression:
    #Features: Square footage, Target: Price in USD
    X = np.array([[600], [800], [1000], [1200], [1500], [2000]])
    y = np.array([150000, 200000, 250000, 290000, 360000, 480000])

    model = LinearRegression()
    model.fit(X, y)

    return model

if __name__ == "__main__":
    model = train_price_model()

    #Test prediction for a new house size
    target_size = np.array([[1300]])
    predicted_price = model.predict(target_size)[0]

    print(f"Predicted price for {target_size[0][0]} sqft: ${predicted_price:,.2f}")