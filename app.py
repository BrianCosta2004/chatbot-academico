from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from calendar_service import get_events
import ollama

app = Flask(__name__)
load_dotenv()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")

    try:
        eventos = get_events()
        response = ollama.chat(
            model='llama3',
            messages=[
                {"role": "system",
                 "content": f"Você é um assistente com acesso à agenda do usuário. Aqui estão os eventos do dia: {eventos} caso necessário, se a solicitação do usuário não necessitar da agenda, então apenas responda o que foi solicitado e responda tudo em português-br"},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['message']['content'].strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": f"Erro ao gerar resposta: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
