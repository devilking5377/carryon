function load() {
  chrome.storage.sync.get(["API_BASE_URL", "auto", "target"], (cfg) => {
    document.getElementById("api").value = cfg.API_BASE_URL || "https://carryon-summarizer.vercel.app"
    document.getElementById("auto").checked = cfg.auto ?? true
    document.getElementById("target").value = cfg.target || 16
    const status = document.getElementById("status")
    if (status) status.textContent = (cfg.API_BASE_URL || "https://carryon-summarizer.vercel.app") ? "API configured" : "Set API Base URL"
  })
}

function save() {
  const API_BASE_URL = document.getElementById("api").value.trim()
  const auto = document.getElementById("auto").checked
  const target = parseInt(document.getElementById("target").value, 10)
  chrome.storage.sync.set({ API_BASE_URL, auto, target })
  const status = document.getElementById("status")
  if (status) status.textContent = "Settings saved"
}

document.getElementById("save").addEventListener("click", save)
document.addEventListener("DOMContentLoaded", load)
