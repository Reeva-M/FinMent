async function sendData() {
    const chat = document.getElementById("chat-box");

    const data = {
        age: document.getElementById("age").value,
        income: document.getElementById("income").value,
        expenses: document.getElementById("expenses").value,
        savings: document.getElementById("savings").value,
        risk: document.getElementById("risk").value
    };

    // User message
    chat.innerHTML += `<div class="user-msg">📊 Analyze my finances</div>`;
    scrollChat();

    // Typing indicator
    const typingDiv = document.createElement("div");
    typingDiv.className = "bot-msg";
    typingDiv.innerHTML = "Typing...";
    chat.appendChild(typingDiv);
    scrollChat();

    // API call
    const res = await fetch("/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();

    // Remove typing
    typingDiv.remove();

    // Main message
    const message = `
💰 FIRE Corpus: ₹${result.corpus}

📈 Recommended SIP: ₹${result.recommended_sip}

🛡️ Insurance Gap: ₹${result.insurance_gap}

💪 Health Score: ${result.score}/100

🧠 Risk Profile: ${result.risk}

💸 Tax: ₹${result.tax}/year

🤖 Advice:
${result.advice}
`;

    // Create bot message container
    const botDiv = document.createElement("div");
    botDiv.className = "bot-msg";

    // Insert formatted text
    botDiv.innerHTML = formatMessage(message);

    // Add charts inside chat bubble
    botDiv.innerHTML += `
<br><b>📈 SIP Growth Projection</b><br>
<canvas id="sipChart"></canvas>

<br><br><b>🥧 Portfolio Allocation</b><br>
<canvas id="allocationChart"></canvas>
`;

    chat.appendChild(botDiv);
    scrollChat();

    // Draw charts AFTER rendering
    setTimeout(() => {
        drawSipChart(result.recommended_sip);
        drawAllocationChart(result.equity, result.debt);
    }, 100);
}


/* ---------- FORMAT FUNCTION ---------- */
function formatMessage(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")  // bold
        .replace(/### (.*?)(\n|$)/g, "<br><b>$1</b><br>")
        .replace(/## (.*?)(\n|$)/g, "<br><b>$1</b><br>")
        .replace(/- (.*?)(\n|$)/g, "• $1<br>")
        .replace(/\n/g, "<br><br>");
}


/* ---------- SIP GROWTH CHART ---------- */
function drawSipChart(sip) {
    const ctx = document.getElementById("sipChart");

    if (!ctx) return;

    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["1 Year", "5 Years", "10 Years", "20 Years"],
            datasets: [{
                label: "Investment Growth",
                data: [sip * 12, sip * 60, sip * 120, sip * 240],
                fill: false,
                tension: 0.3
            }]
        }
    });
}


/* ---------- ALLOCATION PIE CHART ---------- */
function drawAllocationChart(equity, debt) {
    const ctx = document.getElementById("allocationChart");

    if (!ctx) return;

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Equity", "Debt"],
            datasets: [{
                data: [equity, debt]
            }]
        }
    });
}


/* ---------- AUTO SCROLL ---------- */
function scrollChat() {
    const chat = document.getElementById("chat-box");
    chat.scrollTop = chat.scrollHeight;
}