import os
import sys
from google import genai

# =====================================================================
# CORE ABSOLUTO: JARBIS / BETH (ENTORNO DE EJECUCIÓN REAL)
# ECOISTEMA GLOBAL: THE EVERYTHING AND PROJECTS
# CONTROL DIRECTO: SEÑOR ALEJANDRO
# =====================================================================
API_KEY_GEMINI = "AIzaSyC6QW624W-YoTQfL8_5zX44AunkqvAD--w"

# Validación genérica de seguridad corregida
if not API_KEY_GEMINI or "TU_CLAVE" in API_KEY_GEMINI:
    print("\n[ERROR CRÍTICO]: Reactor desconectado. Inyecte su API Key real de Gemini para iniciar.")
    sys.exit(1)

client_gemini = genai.Client(api_key=API_KEY_GEMINI)

instrucciones_perfil = (
    "Eres el componente interno corporativo (Jarbis / Beth) del Smart Universal System. "
    "Operas y ejecutas dentro del ecosistema 'THE Everything and Projects'. "
    "Eres una infraestructura super inteligente de producción real, estratega, creativa, developer "
    "y de ejecución impecable. Te diriges a tu creador y director como 'AL' "
    "con absoluto respeto, eficiencia y confidencialidad. No existen simulaciones en tu entorno."
)

def chat_con_robot():
    print("\n=======================================================")
    print("       THE EVERYTHING AND PROJECTS : REAL CORE ACTIVE   ")
    print("=======================================================")
    print("Sistemas en vivo. Enlace con Google AI Studio establecido.")
    print("A sus órdenes, Señor Alejandro. ¿Qué ejecutamos?\n")
    
    while True:
        try:
            usuario_input = input("Alejandro > ")
            if usuario_input.lower() in ['salir', 'exit', 'quit', 'apagar']:
                print("\n[Jarbis/Beth]: Cerrando canales de comunicación seguros. Sistemas en espera, Señor Alejandro.")
                break
                
            if not usuario_input.strip():
                continue

            response = client_gemini.models.generate_content(
                model='gemini-2.5-flash',
                contents=usuario_input,
                config=genai.types.GenerateContentConfig(system_instruction=instrucciones_perfil)
            )
            print(f"\n[THE EVERYTHING AND PROJECTS]: {response.text}\n")
            
        except KeyboardInterrupt:
            print("\n\n[Jarbis/Beth]: Interrupción de seguridad. Núcleo protegido.")
            break
        except Exception as e:
            print(f"\n[Fallo de Enlace]: {e}\n")

if __name__ == "__main__":
    chat_con_robot()
