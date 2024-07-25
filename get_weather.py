from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_info = None
    if request.method == 'POST':
        city_name = request.form.get('city')
        if city_name:
            url = f'https://wttr.in/{city_name}?format=j1'
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raises an HTTPError for bad responses
                result = response.json()
                
                # Ensure that the expected keys are present
                if 'current_condition' in result:
                    current_condition = result['current_condition'][0]
                    weather_info = {
                        "city": city_name,
                        "weather": current_condition['weatherDesc'][0]['value'],
                        "temperature": current_condition['temp_C'],
                        "feels_like": current_condition['FeelsLikeC'],
                        "humidity": current_condition['humidity']
                    }
                else:
                    weather_info = {"error": "Unexpected response format from API"}
            except requests.exceptions.RequestException as e:
                weather_info = {"error": f"Request failed: {e}"}
            except ValueError as e:
                weather_info = {"error": f"JSON decode error: {e}"}
    
    return render_template('index.html', weather_info=weather_info)

if __name__ == "__main__":
    app.run(debug=True)
