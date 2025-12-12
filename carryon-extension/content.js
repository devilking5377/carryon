function textFrom(el) {
  return (el && (el.innerText || '').trim()) || ''
}

function getSelectionText() {
  const sel = window.getSelection()
  return sel ? (sel.toString() || '').trim() : ''
}

function takeLastTexts(nodes, limit) {
  const arr = Array.from(nodes)
  const last = arr.slice(-limit)
  const out = []
  const seen = new Set()
  last.forEach(n => {
    const t = textFrom(n)
    if (t && !seen.has(t)) { out.push(t); seen.add(t) }
  })
  return out.join('\n\n').trim()
}

function siteSpecific() {
  const host = location.hostname || ''
  if (host.includes('chat.openai.com')) {
    const turns = document.querySelectorAll('[data-testid="conversation-turn"], div[data-message-author-role], .markdown')
    const t = takeLastTexts(turns, 20)
    if (t && t.length > 80) return t
  }
  if (host.includes('claude.ai')) {
    const msgs = document.querySelectorAll('[data-testid*="message"], div[class*="Message"], article')
    const t = takeLastTexts(msgs, 20)
    if (t && t.length > 80) return t
  }
  if (host.includes('poe.com')) {
    const msgs = document.querySelectorAll('[data-testid*="message"], div[class*="Messages"], article')
    const t = takeLastTexts(msgs, 20)
    if (t && t.length > 80) return t
  }
  if (host.includes('perplexity.ai')) {
    const prose = document.querySelectorAll('article, div[class*="prose"], div[class*="answer"]')
    const t = takeLastTexts(prose, 20)
    if (t && t.length > 80) return t
  }
  if (host.includes('gemini.google.com')) {
    const resp = document.querySelectorAll('div[class*="response"], article, div[role="article"]')
    const t = takeLastTexts(resp, 20)
    if (t && t.length > 80) return t
  }
  if (host.includes('bing.com') || host.includes('copilot.microsoft.com')) {
    const msgs = document.querySelectorAll('cib-message, div[class*="cib"] article, div[class*="message"]')
    const t = takeLastTexts(msgs, 20)
    if (t && t.length > 80) return t
  }
  return ''
}

function genericDetect() {
  const selected = getSelectionText()
  if (selected && selected.length > 60) return selected
  const containers = [
    'div[class*="chat"]', 'div[id*="chat"]', 'main[class*="chat"]', 'section[class*="chat"]',
    'div[class*="conversation"]', 'div[id*="conversation"]', 'main[class*="conversation"]',
    'div[class*="thread"]', 'div[class*="messages"]', 'div[class*="dialog"]',
    'div[role="main"]'
  ]
  for (const sel of containers) {
    const c = document.querySelector(sel)
    if (c) {
      const t = takeLastTexts(c.querySelectorAll('div, article, p, li'), 60)
      if (t && t.length > 120) return t
    }
  }
  const blocks = Array.from(document.querySelectorAll('p, li, article, div'))
    .map(el => textFrom(el))
    .filter(t => t && t.length > 30)
  if (blocks.length) {
    blocks.sort((a, b) => b.length - a.length)
    return blocks.slice(0, 40).join('\n\n').trim()
  }
  return (document.body && document.body.innerText) ? document.body.innerText.trim() : ''
}

function detectChatText() {
  const s = siteSpecific()
  if (s && s.length > 80) return s
  return genericDetect()
}

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg && msg.type === 'GET_CHAT_TEXT') {
    try {
      const t = detectChatText()
      sendResponse({ ok: true, text: t })
    } catch (e) {
      sendResponse({ ok: false, error: 'failed_to_detect' })
    }
    return true
  }
})
