import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    # Ahora le decimos a Flask que cargue la interfaz visual que creamos arriba
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    return jsonify({"response": "Canal de IA listo para recibir transmisiones de Acode"})

if __name__ == '__main__':
    app.run(debug=True)
