from flask import Flask, jsonify, request

# creating the Flask application
app = Flask(__name__)

@app.route('/')
def get_hw():
    return "Hello World!"
