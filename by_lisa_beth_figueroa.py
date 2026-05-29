import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    return jsonify({"response": "Enlace del centro de mando listo"})

if __name__ == '__main__':
    app.run(debug=True)
