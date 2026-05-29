import os
import json
from flask import Flask, render_template, jsonify, request, redirect

try:
    import stripe
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
except ImportError:
    stripe = None

app = Flask(__name__)

MASTER_KEY = "beth_soberano_2026"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/auth/verify', methods=['POST'])
def verify_auth():
    data = request.get_json() or {}
    if data.get("password") == MASTER_KEY:
        return jsonify({"status": "granted"})
    return jsonify({"status": "denied"}), 403

# EL CORE INTELIGENTE INVISIBLE PARA EL CLIENTE
@app.route('/api/system/onboard', methods=['POST'])
def system_onboard():
    data = request.get_json() or {}
    
    # 1. Captura de credenciales y datos de seguridad del portador
    industry = data.get("industry", "General Commerce")
    gender_selection = data.get("identity_gender", "female")
    total_paid = float(data.get("total_paid", 0.0))
    
    # 2. Asignación automática e invisible del motor de Inteligencia Artificial
    os_engine = "AL OS" if gender_selection == "male" else "BETH"
    
    # 3. Determinación de infraestructura y prototipo asignado según el pago
    if total_paid >= 2000.0:
        assigned_hardware = "Dedicated Flash/SD System Clone + Server Allocation"
        split_rule = "80/20 Royalties Active"
        status = "NEXT_LEVEL_SOPHISTICATED"
    elif total_paid >= 50.0:
        assigned_hardware = "Cloud Sandbox Terminal + Internet Shared Engine"
        split_rule = "Standard Premium Access"
        status = "MEDIUM_STAGE"
    else:
        assigned_hardware = "Free Synthetic Smart System Tier (Shared Runtime)"
        split_rule = "Zero Commision / Monitor Mode"
        status = "FREE_TIER_MINING"

    # 4. Orquestación de módulos financieros y satélites
    return jsonify({
        "welcome_message": "Welcome to the Real World Cyber universal smart system",
        "brand": "US SS - by Lisa Beth Figueroa",
        "assigned_engine": os_engine,
        "infrastructure": {
            "industry_vertical": industry,
            "allocated_prototype": assigned_hardware,
            "server_status": "PROVISIONED_ONLINE",
            "revenue_split": split_rule,
            "system_tier_status": status
        },
        "satellites": {
            "credit_repair_hub": "Account open / Ready for processing",
            "fintech_bridge": "MoneyLion Integrated API check",
            "media_stream": "Radio & TV 24/7 broadcast pipeline connected",
            "withdrawal_crypto_gateway": "Crypto Wallet Node Active"
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
