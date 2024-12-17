from fastapi import FastAPI, HTTPException                  # Import FastAPI and HTTPException from the fastapi module
from pydantic import BaseModel, Field, field_validator      # Import BaseModel, Field, and field_validator from pydantic
import httpx                                                # Import httpx for making HTTP requests

app = FastAPI()             # Create an instance of the FastAPI class

API_URL = "https://api.openweathermap.org/data/2.5/weather"             # URL for the OpenWeatherMap API

class WeatherRequest(BaseModel):                                # Define a Pydantic model for the request body
    lat: float = Field(..., ge=-90, le=90)                      # Latitude must be between -90 and 90
    lon: float = Field(..., ge=-180, le=180)                    # Longitude must be between -180 and 180
    api_key: str = Field(..., pattern=r'^[a-f0-9]{32}$')        # API key should be a 32-character hexadecimal string

    @field_validator('lat', 'lon')                              # Define a field validator for latitude and longitude
    def validate_coordinates(cls, value):                       # Validator function to ensure coordinates are numbers
        if not isinstance(value, (float, int)):                 # Check if the value is a number
            raise ValueError('Coordinates must be a number')    # Raise an error if not a number
        return value                                            # Return the validated value

@app.post("/weather")                               # Define a POST endpoint at /weather
async def get_weather(request: WeatherRequest):     # Define the request handler function
    params = {                                      # Prepare parameters for the API request
        "lat": request.lat,                         # Latitude from the request
        "lon": request.lon,                         # Longitude from the request
        "appid": request.api_key                    # API key from the request
    }
    async with httpx.AsyncClient() as client:                                            # Create an asynchronous HTTP client
        response = await client.get(API_URL, params=params)                              # Make the API request
        if response.status_code != 200:                                                  # Check if the response status code is not 200
            raise HTTPException(status_code=response.status_code, detail=response.text)  # Raise an HTTP exception
        return response.json()                                                           # Return the response JSON

if __name__ == "__main__":                              # Check if the script is run directly
    import uvicorn                                      # Import uvicorn for running the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)         # Run the FastAPI app on host 0.0.0.0 and port 8000