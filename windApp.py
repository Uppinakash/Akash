import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import requests

app = Flask(__name__)

# Fix the file path warning by using raw string or double backslashes
model = joblib.load(r'Flask\power_prediction.pkl')  # Raw string

@app.route('/')
def home():
    return render_template('intro.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/windapi', methods=['POST'])
def windapi():
    city = request.form.get('city')  # This assumes you are submitting the city via a form in POST method
    apikey = "27482473161ff3fccd89b5265854fcea"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}"
    resp = requests.get(url)
    
    if resp.status_code == 200:
        resp = resp.json()
        temp = str(resp["main"]["temp"]) + " °C"
        humid = str(resp["main"]["humidity"]) + " %"
        pressure = str(resp["main"]["pressure"]) + " mmHG"
        speed = str(resp["wind"]["speed"]) + " m/s"
        return render_template('predict.html', temp=temp, humid=humid, pressure=pressure, speed=speed)
    else:
        return render_template('predict.html', error="City not found or API error.")

@app.route('/y_predict', methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[float(x) for x in request.form.values()]]
    
    prediction = model.predict(x_test)
    print(prediction)
    output = prediction[0]
    return render_template('predict.html', prediction_text='The energy predicted is {:.2f} KWh'.format(output))

if __name__ == "__main__":
    app.run(debug=True)  # Set debug to True for development
