# House Price Prediction

This project uses FastAPI to expose a GET /predict endpoint for house price prediction.

The frontend is served from the same origin at /static/house_form.html, so it can call the API with a relative URL.

The location parameter is optional because the backend gives it a default value of "other".
