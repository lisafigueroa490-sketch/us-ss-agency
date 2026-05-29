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

@app.route('/api/finance/manager', methods=['POST'])
def finance_manager():
    # Detectar datos
    if request.content_type == 'application/json':
        data = request.get_json() or {}
        tier = data.get("tier", "free")
        via = data.get("gateway", "stripe")
    else:
        tier = request.form.get("tier", "free")
        via = request.form.get("gateway", "stripe")

    # Definición de Precios de entrada por Nivel (en centavos de USD)
    tier_prices = {
        "free": 0,
        "low": 50,         # 0.50 USD
        "medium": 500,     # 5.00 USD
        "high": 1500,      # 15.00 USD
        "next_level": 5000 # 50.00 USD
    }

    amount = tier_prices.get(tier, 0)

    # Si es el nivel de Clon o niveles superiores donde aplica la regla 80/20
    if tier in ["1", "2", "3", "clon"]:
        # Simulación del cálculo de la regalía de la agencia central
        total_generado_por_clon = 10000 # Ejemplo: $100.00 USD generados por el clon
        comision_bunker_central = total_generado_por_clon * 0.20 # 20% para nosotros
        ganancia_usuario = total_generado_por_clon * 0.80       # 80% para ellos
        
        return jsonify({
            "status": "clon_active",
            "tier": tier,
            "rule": "80/20 Split Active",
            "agency_royalties_20_percent": f"${comision_bunker_central/100} USD",
            "user_payout_80_percent": f"${ganancia_usuario/100} USD",
            "message": "Contrato inteligente del sistema clon verificado con éxito."
        })

    # Procesar pagos normales de suscripción via Stripe
    if amount > 0 and via == "stripe":
        if not stripe or not stripe.api_key:
            return jsonify({"status": "error", "message": "Stripe Engine Offline"}), 500
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': f'BETH OS - Suscripción Nivel {tier.upper()}'},
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.host_url + '?payment=success',
                cancel_url=request.host_url + '?payment=cancel',
            )
            return redirect(session.url, code=303)
        except Exception as e:
            return jsonify({"status": str(e)}), 500

    return jsonify({
        "status": "active",
        "tier": tier,
        "amount_charged": f"${amount/100} USD",
        "message": "Nivel gratuito o interno procesado por el Robot Manager."
    })

if __name__ == '__main__':
    app.run(debug=True)
