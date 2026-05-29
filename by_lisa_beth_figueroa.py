import os
from flask import Flask, render_template, jsonify, request, redirect

# Intentar importar la librería oficial de Stripe
try:
    import stripe
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
except ImportError:
    stripe = None

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/checkout', methods=['POST'])
def create_checkout_session():
    if not stripe or not stripe.api_key:
        return jsonify({"error": "Stripe no configurado en las variables de entorno de Vercel"}), 500
    
    try:
        # Creamos una sesión de cobro real por un servicio digital
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Servicio de Inteligencia Autónoma - BETH OS',
                        },
                        'unit_amount': 2500, # Monto en centavos (Ejemplo: $25.00 USD)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            # Si el pago es exitoso o cancelado, regresa al centro de mando
            success_url=request.host_url + '?payment=success',
            cancel_url=request.host_url + '?payment=cancel',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    return jsonify({"response": "Enlace del centro de mando listo"})

if __name__ == '__main__':
    app.run(debug=True)
