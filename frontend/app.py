from flask import Flask, request, render_template
import requests

BACKEND_URL = "http://127.0.0.1:5000/formSubmit"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        if request.method == 'GET':
            return render_template('form.html')
        if request.method == 'POST':
            name = request.values.get('name')
            email = request.values.get('email')
            response = requests.post(BACKEND_URL, json={"name": name, "email": email})
            
            if response.status_code == 200:
                return render_template('success.html')
            else:
                try:
                    error_message = response.json().get("error")
                except Exception:
                    error_message = "error occured!."
                return render_template('form.html', error = error_message)
    except requests.exceptions.ConnectionError:
        return render_template("form.html", error="Backend is not running.")



@app.route('/success')
def success():
    
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)