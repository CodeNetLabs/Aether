const filters = [
  "What is", "What is the", "What does", "What happens when", "What are the", "What do you know about",
  "What causes", "What makes", "What kind of", "What would happen if", "How does", "How do", "How can",
  "How is", "How are the", "How does it affect", "How do you know", "How might", "How long does it take to",
  "How often does", "Why is", "Why does", "Why do", "Why can't", "Why should we", "Why did",
  "Why would someone", "Why does it matter if", "Why are there", "Why might", "When did", "When is",
  "When was the last time", "When do", "When should we", "When will", "When can", "When does it become",
  "When was", "When have you seen", "Where is", "Where can", "Where did", "Where does it come from",
  "Where do we find", "Where should we go to", "Where was the first", "Where are the most",
  "Where in the world is", "Where would you look for"
];

function createSummary(text) {
  return text.length > 50 ? text.slice(0, 50) + '...' : text;
}

function welcomeMessage() {
  appendMessage('ai', 'Welcome to Szymdows AI! 😊 I can help you with many things and problems, but I work best with 1-4 word answers!');
}

function cleanQuery(input) {
  let lowered = input.trim();
  for (const phrase of filters) {
    const pattern = new RegExp(`^${phrase}`, 'i');
    if (pattern.test(lowered)) {
      lowered = lowered.replace(pattern, '').trim();
      break;
    }
  }
  return lowered;
}

function isMathExpression(input) {
  return /^[\d\s+\-*/().^%πepisincoqrt]+$/i.test(input);
}

function safeEvalMath(expr) {
  const sanitized = expr
    .replace(/π/gi, 'Math.PI')
    .replace(/e/gi, 'Math.E')
    .replace(/sqrt/gi, 'Math.sqrt')
    .replace(/sin/gi, 'Math.sin')
    .replace(/cos/gi, 'Math.cos')
    .replace(/%/g, '/100')
    .replace(/\^/g, '**');

  return Function('"use strict"; return (' + sanitized + ')')();
}

async function askWiki() {
  const input = document.getElementById('user-input');
  const rawQuery = input.value.trim();
  if (!rawQuery) return;

  appendMessage('user', rawQuery);

  const query = cleanQuery(rawQuery);
  let reply = "I couldn't find anything in my database. 😔 But try to refrase your input or try something else. (Remember that I am still in training!)";

  try {
    if (isMathExpression(query)) {
      const result = safeEvalMath(query);
      reply = `The result is: ${result}`;
    } else {
      const response = await fetch(`https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(query)}`);
      const data = await response.json();
      if (data.extract) {
        const paragraphs = data.extract.split('\n');
        reply = paragraphs.slice(0, 2).join('\n\n');
      }
    }
  } catch (e) {
    reply = "Sorry, I couldn't compute that expression. 😔";
  }

  appendMessage('ai', reply);
  appendHistoryItem(query, reply);

  input.value = '';
}

function appendMessage(sender, text) {
  const log = document.getElementById('chat-log');
  const entry = document.createElement('div');
  entry.className = 'chat-entry ' + sender;
  entry.textContent = `${sender === 'user' ? 'You' : 'Szymdows AI'}: ${text}`;
  log.appendChild(entry);
  log.scrollTop = log.scrollHeight;
}

function appendHistoryItem(query, reply) {
  const history = document.getElementById('history');
  const item = document.createElement('div');
  item.className = 'history-item';
  item.textContent = `${query}: ${createSummary(reply)}`;
  history.prepend(item);
}

document.getElementById('user-input').addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    askWiki();
  }
});

window.onload = welcomeMessage;
