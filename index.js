function sendMessage() {
    let userInput = document.getElementById("user-message").value;
    if (!userInput.trim()) return;

    addMessage(userInput, "user");

    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => addMessage(data.reply, "bot"))
    .catch(error => console.error("Error:", error));

    document.getElementById("user-message").value = "";
}

function addMessage(content, sender) {
    let chatBox = document.getElementById("chat-box");
    let messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
    messageDiv.innerText = content;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
window.onload = async () => {
    const res = await fetch('/history');
    const history = await res.json();
    const replyDiv = document.getElementById("chat-box");
    history.forEach(m => {
        const bubble = document.createElement("div");
        bubble.className = m.role === 'user' ? 'user-bubble' : 'bot-bubble';
        bubble.innerHTML = formatMarkdown(m.content);
        replyDiv.appendChild(bubble);
    });
};
