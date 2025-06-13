from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from calendar_service import get_events

# Ativa o modo de testes (sem usar a OpenAI)
TEST_MODE = True

# Carrega variáveis do .env
load_dotenv()

# Apenas importa o openai se for necessário
if not TEST_MODE:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    if not request.is_json:
        return jsonify({"error": "Requisição precisa ser JSON."}), 400

    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "Mensagem não fornecida."}), 400

    # Consulta agenda se houver palavras-chave
    if "agenda" in user_input.lower() or "compromissos" in user_input.lower() or "hoje" in user_input.lower():
        eventos = get_events()
        if eventos:
            return jsonify({"reply": "Aqui está sua agenda de hoje:\n" + "\n".join(eventos)})
        else:
            return jsonify({"reply": "Você não tem compromissos hoje."})

    if "oi" in user_input.lower() or "ola" in user_input.lower() or "olá" in user_input.lower():
        return jsonify({"reply": "Olá, no que posso ajudar? :)"})

    # Simula resposta se estiver em modo de testes
    if TEST_MODE:
        return jsonify({"reply": f"(Simulado) Você disse: {user_input}"})

    # Chamada real à API da OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente pessoal que responde perguntas gerais."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message['content'].strip()
        return jsonify({"reply": reply})

    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower():
            return jsonify({"reply": "⚠️ Sua conta da OpenAI excedeu a cota de uso da API. Verifique seu plano."})
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)
