import os
from flask import Flask, render_template, jsonify, request, redirect

try:
    import stripe
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
except ImportError:
    stripe = None

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# EL ROBOT MANAGER DE FINANZAS CENTRALIZADO
@app.route('/api/finance/manager', methods=['POST'])
def finance_manager():
    data = request.get_json() or {}
    via = data.get("gateway", "stripe") # Vía por defecto si no se especifica
    amount = data.get("amount", 2500)   # Monto por defecto ($25.00)
    
    # CANAL 1: ORQUESTADOR STRIPE
    if via == "stripe":
        if not stripe or not stripe.api_key:
            return jsonify({"status": "error", "message": "Stripe Engine Offline"}), 500
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': 'BETH OS - Digital Service'}, 'unit_amount': amount}, 'quantity': 1}],
                mode='payment',
                success_url=request.host_url + '?payment=success',
                cancel_url=request.host_url + '?payment=cancel',
            )
            return jsonify({"status": "redirect", "url": session.url})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
            
    # CANAL 2: ORQUESTADOR WISE / TRANSFERENCIA
    elif via == "wise":
        # Aquí el Robot Manager genera las instrucciones de depósito automatizadas de Wise
        profile_id = os.environ.get("WISE_PROFILE_ID", "lisaf1339")
        return jsonify({
            "status": "instructions",
            "gateway": "Wise Global",
            "account_holder": "Lisa Beth Figueroa",
            "profile_reference": profile_id,
            "message": f"Robot Manager ha apartado un folio para depósito de ${amount/100} USD."
        })
        
    # CANAL 3: ORQUESTADOR CRIPTO (Vía de respaldo futura)
    elif via == "crypto":
        return jsonify({
            "status": "crypto_gate",
            "message": "Orquestador Crypto esperando enlace a Wallet Soberana."
        })

    return jsonify({"status": "error", "message": "Vía de pago no identificada por el Robot Manager"}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    return jsonify({"response": "Enlace del centro de mando listo"})

if __name__ == '__main__':
    app.run(debug=True)
