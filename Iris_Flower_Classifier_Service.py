from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

# Initialize the FastAPI application for the ML service
app = FastAPI(
    title="Iris Classification Service",
    description="A machine learning API serving a trained Iris flower classifier.",
    version="1.0.0"
)

# Train a lightweight classification model on startup using the classic Iris dataset
iris = load_iris()
X_train, y_train = iris.data, iris.target
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Define strict input data structure using Pydantic for validation
class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., gt=0, description="Sepal length in cm")
    sepal_width: float = Field(..., gt=0, description="Sepal width in cm")
    petal_length: float = Field(..., gt=0, description="Petal length in cm")
    petal_width: float = Field(..., gt=0, description="Petal width in cm")

@app.post("/predict")
def predict_iris_species(features: IrisFeatures):
    """
    Predicts the Iris flower species based on physical measurements
    with input validation to prevent anomalous data or model exploitation.
    """
    # Security & Reality check: Ensure physical measurements stay within realistic botanical bounds
    if (features.sepal_length > 15.0 or features.sepal_width > 15.0 or 
        features.petal_length > 15.0 or features.petal_width > 15.0):
        raise HTTPException(
            status_code=400,
            detail="Invalid physical measurements: Values exceed realistic botanical bounds."
        )

    # Prepare input array for the Scikit-Learn model
    input_data = [[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width
    ]]

    # Execute model prediction
    prediction = model.predict(input_data)[0]
    species_name = iris.target_names[prediction]

    return {
        "status": "Success",
        "predicted_class_id": int(prediction),
        "species": species_name
    }

if __name__ == "__main__":
    import uvicorn
    # Run the server locally for testing
    uvicorn.run(app, host="127.0.0.1", port=8000)