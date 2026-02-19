from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
print("env loaded!!!")

uri = os.getenv("MONGO_URI")

client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.test
collection = db['flask-assignment']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return {"message": "Welcome to the BACKEND!"}

@app.route('/formSubmit', methods=['POST'])
def formSubmit():
    try:
        data = request.json
        
        collection.insert_one({
            "name": data.get("name"),
            "email": data.get("email")
        })
        return jsonify({"message": "Form submitted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True)