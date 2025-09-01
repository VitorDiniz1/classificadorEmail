import os
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

load_dotenv()

app = Flask(__name__, static_folder="../frontend")
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

API_URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

def process_email_with_gemini(email_content):
    """
    Função para classificar e gerar resposta para um email usando a API do Gemini.
    A API é instruída a retornar um JSON estruturado.
    """
    
    system_prompt = (
        "Você é um assistente de e-mail. Sua tarefa é analisar o conteúdo de um e-mail, "
        "classificá-lo como 'Produtivo' ou 'Improdutivo', e então gerar uma resposta apropriada. "
        "Um e-mail 'Produtivo' é um que requer ação, como uma pergunta, solicitação ou problema. "
        "Um e-mail 'Improdutivo' é um que não requer ação imediata, como um agradecimento, uma saudação cordial ou spam. "
        "A resposta deve ser sempre em um formato JSON."
    )
    
    user_prompt = f"Analise e responda ao seguinte e-mail: '{email_content}'"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_prompt}
                ],
                "role": "user"
            }
        ],
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "classification": {
                        "type": "STRING",
                        "enum": ["Produtivo", "Improdutivo"]
                    },
                    "suggested_reply": {
                        "type": "STRING"
                    }
                },
                "required": ["classification", "suggested_reply"]
            }
        },
    }
    
    try:
        response = requests.post(
            API_URL_GEMINI, 
            params={"key": GEMINI_API_KEY}, 
            json=payload
        )
        response.raise_for_status()
        
        response_data = response.json()
        raw_json_string = response_data['candidates'][0]['content']['parts'][0]['text']
        return json.loads(raw_json_string)

    except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError) as e:
        print(f"Erro na requisição à API do Gemini: {e}")
        return None

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def serve_static(path):
    """Rota para servir os arquivos estáticos (HTML, CSS, JS) do frontend."""
    return send_from_directory(app.static_folder, path)

@app.route("/api/classify", methods=["POST"])
def classify_email():
    """Rota da API para classificar e-mail."""
    data = request.json
    email_content = data.get("email_content")

    if not email_content:
        return jsonify({"error": "Nenhum conteúdo de e-mail fornecido."}), 400

    if not GEMINI_API_KEY:
        return jsonify({"error": "Chave GEMINI_API_KEY não encontrada. Por favor, adicione-a ao seu arquivo .env."}), 500

    try:
        result = process_email_with_gemini(email_content)
        
        if result is None:
            return jsonify({"error": "Ocorreu um erro ao processar o e-mail com a IA."}), 500

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({"error": "Ocorreu um erro interno no servidor."}), 500

    return jsonify({
        "classification": result.get("classification"),
        "suggested_reply": result.get("suggested_reply")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

