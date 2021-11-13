import requests
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import json, pprint
import datetime, math, os
from application import db
from application.models import City
from application import app


def get_weather_data(city_name):
    api_key = os.environ['weather_data']
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url).json()
    # pprint.pprint(response)
    return response

def get_time(timezone):
    tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
    return datetime.datetime.now(tz = tz).strftime("%H:%M")
def get_date(date):
    tz = datetime.timezone(datetime.timedelta(seconds=int(date)))
    return datetime.datetime.now(tz = tz).strftime("%A, %B %d, %Y.")

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(int(time)).strftime('%I:%M %p')
    return converted_time

def mps_to_kmph(mps):
    return (3.6 * mps)

def wind_deg(deg):
    compassPoints = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    rawPosition = math.floor((deg / 22.5) + 0.5);
    arrayPosition = (rawPosition % 16);
    return compassPoints[arrayPosition];

def visibility_m_to_km(km):
    return (km / 1000)

@app.route("/")
@app.route("/home")
def index_get():
    page_tittle = "WeatherApp | Vuk Lekić"       
    cities = City.query.all()  
    weather_data = []
    for city_name in cities:
        response = get_weather_data(city_name.name)
        # pprint.pprint(response)
    
        weather = {
            'city' : city_name.name,
            'temperature' : int(response['main']['temp']),
            'realfeel' : int(response['main']['feels_like']),
            'description' : response['weather'][0]['description'],
            'icon' : response['weather'][0]['icon'],
            'date' : f"{get_date(response['timezone'])}",
            'time': f"{get_time(response['timezone'])}",
            'country' : response['sys']['country'],
            'humidity' : response['main']['humidity'],
            'cloud' : response['clouds']['all'],
            'deg' : f"{wind_deg(response['wind']['deg'])}",
            'wind' : f"{round(mps_to_kmph(response['wind']['speed']),1)}",
            'visibility' : f"{round(visibility_m_to_km(response['visibility']))}",
        }
        weather_data.append(weather)
        # pprint.pprint(weather)

    return render_template('weather.html', page_tittle=page_tittle, weather_data=weather_data)

@app.route("/")
@app.route("/home")
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
    if new_city:
        exist_city = City.query.filter_by(name=new_city).first()
        if not exist_city:
            new_city_data = get_weather_data(new_city)
            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city) 
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = 'City does not exist!'
        else:
            err_msg = 'City already exists!'
    elif not new_city:
                err_msg = 'Please enter a city name!'
    
    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added successfully!')
    
    return redirect(url_for('index_get'))

@app.route("/delete/<name>/")
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()
    flash(f'Successfully deleted {city.name}', 'success')
    return redirect(url_for('index_get'))
