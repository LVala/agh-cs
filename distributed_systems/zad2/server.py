from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import os
import time
import httpx
import asyncio

RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]
GEODB_HOST = "wft-geo-db.p.rapidapi.com"

WEATHERAPI_KEY = os.environ["WEATHERAPI_KEY"]
WEATHERAPI_HOST = "api.weatherapi.com"

PERMITTED_KEYS = ["1234"]

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = [f"{error['loc'][1]} - {error['msg']}" for error in exc.errors()]

    return templates.TemplateResponse("error.html", {
        "request": request,
        "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "detail": ", ".join(messages)
        })

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("error.html", {
        "request": request,
        "status_code": exc.status_code,
        "detail": exc.detail
        })

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return  templates.TemplateResponse("form.html", {"request": request})

@app.get("/weather", response_class=HTMLResponse)
async def weather(request: Request, city: str, radius: int = 0, days: int = 1, key: str | None = None):
    if key is None:
        raise HTTPException(status_code=401, detail="Validation key is not present")
    if key not in PERMITTED_KEYS:
        # TODO generate keys dynamically
        raise HTTPException(status_code=403, detail="Validation key does not have required permission to access requested content")
    if radius < 1 or radius > 100:
        raise HTTPException(status_code=400, detail="Radius should be an integer between 1 and 100")
    if days < 1 or days > 14:
        raise HTTPException(status_code=400, detail="Days should be an integer between 1 and 14")

    cities = get_cities(city, radius)
    weathers = await get_weathers(cities, days)

    temps_now = [city["current"]["temp_c"] for city in weathers]
    avg_temp_now = sum(temps_now) / len(temps_now)

    feelslikes_now = [city["current"]["feelslike_c"] for city in weathers]
    avg_feelslike_now = sum(feelslikes_now) / len(feelslikes_now)

    forecast_by_day = [[weathers[city]["forecast"]["forecastday"][day] for city in range(len(cities))] for day in range(days)]

    get_temps = lambda name: [max([city["day"][name] for city in forecast_by_day[day]]) for day in range(days)]

    dates = [day[0]["date"] for day in forecast_by_day]
    max_temp_by_day = get_temps("maxtemp_c") 
    min_temp_by_day = get_temps("mintemp_c") 
    avg_temp_by_day = get_temps("avgtemp_c") 

    forecast = [{
        "date": dates[day], 
        "max": max_temp_by_day[day], 
        "min": min_temp_by_day[day],
        "avg": avg_temp_by_day[day],
        } for day in range(days)]

    return templates.TemplateResponse("weather.html", {
        "request": request,
        "cities": [city["name"] for city in cities],
        "days": days,
        "avg_temp_now": avg_temp_now,
        "avg_feelslike_now": avg_feelslike_now,
        "forecast": forecast,
        })

def get_cities(city_name: str, radius: int):
    url = f"https://{GEODB_HOST}/v1/geo/cities"
    headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": GEODB_HOST
            }
    params = {
            "namePrefix": city_name,
            "limit": 1,
            "sort": "-population"
            }

    try:
        response = httpx.get(url, params=params, headers=headers).json()
        json_data = response["data"]
    except (httpx.HTTPError, KeyError):
        raise HTTPException(status_code=502, detail="Unable to request city informations")

    if len(json_data) == 0:
        raise HTTPException(status_code=404, detail="City not found")

    location = [json_data[0]["latitude"], json_data[0]["longitude"]]

    for i in range(len(location)):
        location[i] = str(location[i])
        if location[i][0] != "-": location[i] = "+" + location[i]

    latitude, longitude = location

    time.sleep(1)  # limit of 1 request per second on the GeoDB Cities api

    url = f"https://{GEODB_HOST}/v1/geo/locations/{latitude}{longitude}/nearbyCities"
    params = {"radius": radius, "limit": 10, "sort": "-population"}

    try:
        response = httpx.get(url, headers=headers, params=params).json()
        json_data = response["data"]
    except (httpx.HTTPError, KeyError):
        raise HTTPException(status_code=502, detail="Unable to request city informations")

    return json_data

async def get_weathers(cities, days):
    url = f"https://{WEATHERAPI_HOST}/v1/forecast.json" 
    params = {
            "key": WEATHERAPI_KEY,
            "hour": 17,
            "alerts": "no",
            "aqi": "no",
            "days": days
            }

    async with httpx.AsyncClient() as client:
        tasks = [] 
        for city in cities:
            params["q"] = f"{city['latitude']},{city['longitude']}"
            request = client.get(url, params=params)
            tasks.append(request)
        try:
            responses = await asyncio.gather(*tasks)
            json_data = [response.json() for response in responses]
        except (httpx.HTTPError, KeyError):
            raise HTTPException(status_code=502, detail="Unable to request weather information")

    return json_data
