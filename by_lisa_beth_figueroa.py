import os
import json
from flask import Flask, render_template, jsonify, request, redirect

try:
    import stripe
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
except ImportError:
    stripe = None

app = Flask(__name__)

# Simulador de persistencia de datos (Local Logs que emulan sincronización con Google Drive)
DRIVE_LOG_FILE = "google_drive_sync.json"

def save_to_drive_emulator(event_type, details):
    """Guarda un registro nanométrico simulando el puente hacia Google Drive"""
    log_entry = {"event": event_type, "details": details}
    try:
        if os.path.exists(DRIVE_LOG_FILE):
            with open(DRIVE_LOG_FILE, "r+") as f:
                data = json.load(f)
                data.append(log_entry)
                f.seek(0)
                json.dump(data, f, indent=2)
        else:
            with open(DRIVE_LOG_FILE, "w") as f:
                json.dump([log_entry], f, indent=2)
    except Exception:
        pass

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/finance/manager', methods=['POST'])
def finance_manager():
    # Detectar si la petición viene de un formulario web tradicional o de un JSON
    if request.content_type == 'application/json':
        data = request.get_json() or {}
        via = data.get("gateway", "stripe")
        amount = data.get("amount", 2500)
    else:
        via = request.form.get("gateway", "stripe")
        amount = int(request.form.get("amount", 2500))

    # CANAL 1: STRIPE & GOOGLE PAY ORQUESTADOR
    if via == "stripe":
        if not stripe or not stripe.api_key:
            save_to_drive_emulator("STRIPE_ERROR", "Intento de cobro fallido: Engine Offline")
            return jsonify({"status": "error", "message": "Stripe Engine Offline en Vercel"}), 500
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'], # Stripe maneja automáticamente Google Pay aquí
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'BETH OS - Módulo de Finanzas Activo'},
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.host_url + '?payment=success',
                cancel_url=request.host_url + '?payment=cancel',
            )
            save_to_drive_emulator("STRIPE_REDIRECT", f"Sesión creada por {amount/100} USD")
            return redirect(session.url, code=303)
        except Exception as e:
            save_to_drive_emulator("STRIPE_CRASH", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500
            
    # CANAL 2: WISE GLOBAL VÍA
    elif via == "wise":
        profile_id = os.environ.get("WISE_PROFILE_ID", "lisaf1339")
        account_details = {
            "gateway": "Wise System Interconnected",
            "account_holder": "Lisa Beth Figueroa",
            "profile_reference": profile_id,
            "amount_usd": amount / 100
        }
        save_to_drive_emulator("WISE_INVOICE_GENERATED", account_details)
        return jsonify({
            "status": "instructions",
            "message": "Ficha de depósito generada por el Robot Manager",
            "details": account_details
        })

    return jsonify({"status": "error", "message": "Canal no identificado"}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    return jsonify({"response": "Enlace del centro de mando listo"})

if __name__ == '__main__':
    app.run(debug=True)
