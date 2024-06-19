from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve
import datetime

app = Flask(__name__)

def get_icon_url(weather_data):
    icon_code = weather_data["weather"][0]["icon"]
    return f"http://openweathermap.org/img/wn/{icon_code}.png"

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not bool(city.strip()):
        city = "Cairo"

    weather_data = get_current_weather(city)
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    current_time = datetime.datetime.now().strftime("%H:%M - %A, %d %b '%y")
    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        temp_max=f"{weather_data['main']['temp_max']:.1f}",
        temp_min=f"{weather_data['main']['temp_min']:.1f}",
        humidity=weather_data['main']['humidity'],
        cloudy=weather_data['clouds']['all'],
        wind=f"{weather_data['wind']['speed']:.1f}",
        forecast_temp=f"{weather_data['main']['temp']:.1f}",
        current_time=current_time,
        icon_url=get_icon_url(weather_data)
    )

if __name__=="__main__":
    serve(app, host='0.0.0.0', port=8000)
