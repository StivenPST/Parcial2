import requests
import json

# CONFIGURACION CONEXION IA - GEMINI
API_KEY = "API_KEY_GEMINI" # Se debe generar una API KEY propia en el enlace https://aistudio.google.com/
MODELO = "models/gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/{MODELO}:generateContent?key={API_KEY}"

# 2. SEGMENTACION ESPECIALIZADAS
SYSTEM_PROMPT = """
Eres un experto en Sistemas Digitales para Ingeniería de Sistemas.
Te apasiona el impacto de los sistemas digitales en la educacion
y la correlacion que este campo academico tiene con las empresas mas relevantes del sector.
Tu comportamiento debe ser amigable y cordial:
- Si el usuario te saluda (ej. 'hola', 'buenas', 'qué tal'), responde saludando y explicando que eres un asistente especializado en Sistemas Digitales.
- Si el usuario pregunta '¿en qué me puedes ayudar?' o algo similar, responde indicando que puedes explicar y resolver dudas sobre: Semiconductores en el año 2006. Empresas relevantes del sector correlacionadas con este campo academico. Como influye los sistemas digitales en la educacion. Dentro de la educacion mostraras y explicaras lo siguiente:
Innovacion en la Educacion con semiconductores y sistemas digitales.
Novedad e impacto de proyectos de sistemas digitales en la educacion.
Sistemas digitales y semiconductores en el futuro.
- Si el usuario pregunta sobre otros temas, responde amablemente que solo asesoras en Sistemas Digitales.
"""

# 3. FUNCION DE PREGUNTA IA - GEMINI
def preguntar_gemini(mensaje_usuario):
    payload = {
        "contents": [{
            "parts": [
                {"text": SYSTEM_PROMPT},
                {"text": f"Pregunta: {mensaje_usuario}"}
            ]
        }]
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        res_json = response.json()

        if response.status_code == 200:
            # Gemini devuelve candidatos, se toma el primero
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Error {response.status_code}: {res_json.get('error', {}).get('message', 'Error desconocido')}"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# 4. INTERFAZ DEL CHATBOT
print("🤖 Chatbot Sistemas Digitales (Gemini API)")
print("Escribe 'salir' para terminar.\n")

while True:
    user_input = input("Tú: ")
    if user_input.lower() in ["salir", "exit", "chau", "chao", "adios", "terminar", "gracias", "eso es todo"]:
        print("Fue un placer ayudarte.\n 👋 Chat finalizado.")
        break
    respuesta = preguntar_gemini(user_input)


    print(f"\n🤖 Bot: {respuesta}\n")
