function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    appendMessage("Você", message);
    input.value = "";

    fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
})
.then(async response => {
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || "Erro desconhecido no servidor.");
    }
    return response.json();
})
.then(data => {
    if (data.reply) {
        appendMessage("Assistente", data.reply);
    } else {
        appendMessage("Assistente", "Erro ao responder.");
    }
})
.catch(err => {
    appendMessage("Assistente", "Erro de conexão com o servidor: " + err.message);
});
}

function appendMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");
    const msg = document.createElement("div");
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}
