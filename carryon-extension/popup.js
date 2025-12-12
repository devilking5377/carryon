const DEFAULT_API_BASE = 'http://localhost:5000'

async function getConfig() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(["API_BASE_URL", "auto", "target"], (cfg) => resolve(cfg || {}))
  })
}

function setStatus(text, type = "info") {
  const el = document.getElementById('status')
  if (!el) return
  el.textContent = text || ''
}

document.getElementById('openOptions').addEventListener('click', () => {
  if (chrome.runtime.openOptionsPage) chrome.runtime.openOptionsPage()
})

async function summarize(text, target) {
  const cfg = await getConfig()
  const base = cfg.API_BASE_URL || DEFAULT_API_BASE
  const url = base ? `${base}/api/summarize` : '/api/summarize'
  const body = target ? { text, target_sentences: target } : { text }
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error('Failed to summarize')
  const data = await res.json()
  return data.summary || ''
}

document.getElementById('grab').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true })
  const [{result}] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => window.getSelection().toString(),
  })
  document.getElementById('input').value = result || ''
})

document.getElementById('run').addEventListener('click', async () => {
  const input = document.getElementById('input').value.trim()
  const auto = document.getElementById('auto').checked
  const target = parseInt(document.getElementById('target').value, 10)
  if (!input) return
  setStatus('Summarizing…')
  const runBtn = document.getElementById('run')
  runBtn.disabled = true
  try {
    const text = await summarize(input, auto ? undefined : target)
    document.getElementById('summary').textContent = text
    setStatus('Done')
  } catch (e) {
    document.getElementById('summary').textContent = ''
    setStatus('Error: could not create summary.')
  }
  runBtn.disabled = false
})

document.getElementById('copy').addEventListener('click', async () => {
  const text = document.getElementById('summary').textContent
  if (text) await navigator.clipboard.writeText(text)
})

document.getElementById('download').addEventListener('click', () => {
  const text = document.getElementById('summary').textContent
  if (!text) return
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'summary.txt'
  a.click()
  URL.revokeObjectURL(url)
})

document.getElementById('save').addEventListener('click', async () => {
  const val = document.getElementById('api').value.trim()
  const auto = document.getElementById('auto').checked
  const target = parseInt(document.getElementById('target').value, 10)
  chrome.storage.sync.set({ API_BASE_URL: val, auto, target })
  setStatus('Settings saved')
})

window.addEventListener('DOMContentLoaded', async () => {
  const cfg = await getConfig()
  document.getElementById('api').value = cfg.API_BASE_URL || DEFAULT_API_BASE
  document.getElementById('auto').checked = cfg.auto ?? true
  document.getElementById('target').value = cfg.target || 16
  setStatus((cfg.API_BASE_URL || DEFAULT_API_BASE) ? 'API configured' : 'Set API in Advanced')

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true })
    const resp = await chrome.tabs.sendMessage(tab.id, { type: 'GET_CHAT_TEXT' })
    if (resp && resp.ok && resp.text && resp.text.length > 80) {
      document.getElementById('input').value = resp.text
      // auto-run summarize
      const auto = document.getElementById('auto').checked
      const target = parseInt(document.getElementById('target').value, 10)
      setStatus('Auto-detected chat text')
      const text = await summarize(resp.text, auto ? undefined : target)
      document.getElementById('summary').textContent = text
      setStatus('Done')
    }
  } catch (e) {
    
  }
})
