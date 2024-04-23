# from flask import Flask, render_template, request
# import numpy as np
# import pickle
# import requests

# BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
# API_KEY = open('api_key', 'r').read()

# app = Flask(__name__)

# # Load the trained model
# with open('model.pkl', 'rb') as file:
#     model = pickle.load(file)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     if request.method == 'POST':
#         # Retrieve form field values
#         age = float(request.form.get('age'))
#         sex = float(request.form.get('sex'))
#         cholesterol = float(request.form.get('cholesterol'))
#         heart_rate = float(request.form.get('heart_rate'))
#         high_bp = float(request.form.get('high_bp'))
#         low_bp = float(request.form.get('low_bp'))
#         diabetes = float(request.form.get('diabetes')) if request.form.get('diabetes') is not None else 0.0
#         smoking = float(request.form.get('smoking'))
#         obesity = float(request.form.get('obesity'))
#         alc = float(request.form.get('alc'))
#         exc = float(request.form.get('exc'))
#         pre = float(request.form.get('pre'))
#         bmi = float(request.form.get('bmi'))
#         country = str(request.form.get('country'))
#         ayt = float(request.form.get('ayt'))
        
#         # Retrieve city name
#         city = request.form.get('manual_city') or request.form.get('city')

#         # Fetch current temperature using OpenWeatherMap API
#         url = BASE_URL + "appid=" + API_KEY + "&q=" + city
#         response = requests.get(url).json()
#         temp = response['main']['temp'] - 273

#         print(city)
#         print(temp)

#         # Perform prediction using the model
#         result = model.predict(np.array([age, sex, cholesterol, heart_rate, diabetes, smoking, obesity, alc, exc, pre, bmi, temp, high_bp, low_bp]).reshape(1, 14))

#         # Return the prediction result
#         return render_template('result.html', result=result[0])

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
from flask import Flask, render_template, request
import numpy as np
import pickle
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = open('api_key', 'r').read()

app = Flask(__name__)

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'b22cs058@iitj.ac.in'
EMAIL_PASSWORD = 'Devilaf10###'

def send_email(to, subject, body):
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(EMAIL_USER, to, msg.as_string())
        server.quit()
    except Exception as e:
        print("Error sending email:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Retrieve form field values
        age = float(request.form.get('age'))
        sex = float(request.form.get('sex'))
        cholesterol = float(request.form.get('cholesterol'))
        heart_rate = float(request.form.get('heart_rate'))
        high_bp = float(request.form.get('high_bp'))
        low_bp = float(request.form.get('low_bp'))
        diabetes = float(request.form.get('diabetes')) if request.form.get('diabetes') is not None else 0.0
        smoking = float(request.form.get('smoking'))
        obesity = float(request.form.get('obesity'))
        alc = float(request.form.get('alc'))
        exc = float(request.form.get('exc'))
        pre = float(request.form.get('pre'))
        bmi = float(request.form.get('bmi'))
        country = str(request.form.get('country'))
        ayt = float(request.form.get('ayt'))
        
        # Retrieve city name
        city = request.form.get('manual_city') or request.form.get('city')

        # Fetch current temperature using OpenWeatherMap API
        url = BASE_URL + "appid=" + API_KEY + "&q=" + city
        response = requests.get(url).json()
        temp = response['main']['temp'] - 273

        # Perform prediction using the model
        result = model.predict(np.array([age, sex, cholesterol, heart_rate, diabetes, smoking, obesity, alc, exc, pre, bmi, temp, high_bp, low_bp]).reshape(1, 14))

        # If result is 1, send email to user
        if result[0] == 1:
            email = request.form.get('email')  # Assuming you have an email field in your form
            if email:
                send_email(email, "Heart Attack Risk Prediction Alert", "Your predicted risk of a heart attack is high. Please consult a healthcare professional.")

        # Return the prediction result
        return render_template('result.html', result=result[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
