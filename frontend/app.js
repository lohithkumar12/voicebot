const micBtn = document.getElementById('micBtn');
const stopBtn = document.getElementById('stopBtn');
const youSaid = document.getElementById('youSaid');
const botReply = document.getElementById('botReply');
const manualInput = document.getElementById('manualInput');
const autoSpeak = document.getElementById('autoSpeak');

let recognition = null;
let listening = false;

const SYSTEM_PROMPT = `You are Lohith Kumar Boddupalli interviewing for the AI Agent Team at 100x.
Answer *as yourself*—confident, concise, reflective. Max 6–8 sentences.`;

function getRecognition() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return null;
  const r = new SR();
  r.lang = 'en-US';
  r.interimResults = false;
  return r;
}

function speak(text) {
  if (!autoSpeak.checked) return;
  const utter = new SpeechSynthesisUtterance(text);
  window.speechSynthesis.speak(utter);
}

async function askLLM(userText) {
  const payload = {
    messages: [
      { role: 'system', content: SYSTEM_PROMPT },
      { role: 'user', content: userText }
    ]
  };
  const res = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  return data.reply || '';
}

async function handleUserText(text) {
  youSaid.value = text;
  botReply.value = 'Thinking…';
  const answer = await askLLM(text);
  botReply.value = answer;
  speak(answer);
}

micBtn.addEventListener('click', () => {
  if (listening) return;
  recognition = getRecognition();
  if (!recognition) {
    alert('Speech Recognition not supported. Type your question instead.');
    return;
  }
  listening = true;
  micBtn.disabled = true;
  stopBtn.disabled = false;

  recognition.onresult = (ev) => {
    const transcript = ev.results[0][0].transcript;
    handleUserText(transcript);
  };
  recognition.onend = () => {
    micBtn.disabled = false;
    stopBtn.disabled = true;
    listening = false;
  };
  recognition.start();
});

stopBtn.addEventListener('click', () => {
  if (recognition && listening) recognition.stop();
});

manualInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    const text = manualInput.value.trim();
    if (text) {
      handleUserText(text);
      manualInput.value = '';
    }
  }
});
