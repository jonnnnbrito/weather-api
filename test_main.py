from fastapi.testclient import TestClient               # Import TestClient from fastapi.testclient
from main import app                                    # Import the FastAPI app instance from main.py

client = TestClient(app)                                # Create a TestClient instance for testing the FastAPI app

def test_get_weather_valid():                           # Define a test function for valid input
    response = client.post("/weather", json={           # Send a POST request to /weather with valid data
        "lat": -33.86785,                               # Valid latitude
        "lon": 151.20732,                               # Valid longitude
        "api_key": "5f6056026f2837d3f53fbf8970f2f4d9"   # Valid API key
    })
    assert response.status_code == 200                  # Assert that the response status code is 200
    data = response.json()                              # Parse the response JSON
    assert "weather" in data                            # Assert that the response contains the "weather" key
    assert "main" in data                               # Assert that the response contains the "main" key

def test_get_weather_invalid_lat():                     # Define a test function for invalid latitude
    response = client.post("/weather", json={           # Send a POST request to /weather with invalid latitude
        "lat": -100.0,                                  # Invalid latitude
        "lon": 151.20732,                               # Valid longitude
        "api_key": "5f6056026f2837d3f53fbf8970f2f4d9"   # Valid API key
    })
    assert response.status_code == 422                  # Assert that the response status code is 422

def test_get_weather_invalid_api_key():                 # Define a test function for invalid API key
    response = client.post("/weather", json={           # Send a POST request to /weather with invalid API key
        "lat": -33.86785,                               # Valid latitude
        "lon": 151.20732,                               # Valid longitude
        "api_key": "invalidapikey"                      # Invalid API key
    })
    assert response.status_code == 422                  # Assert that the response status code is 422