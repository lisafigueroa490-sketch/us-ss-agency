import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "bunker": "us-ss-agency",
        "message": "Bunker Autonomo Humanless Activo",
        "engine": "Gemini API Key Conectada con Exito"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    return jsonify({"response": "Canal de IA listo para recibir transmisiones de Acode"})

if __name__ == '__main__':
    app.run(debug=True)
