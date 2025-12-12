class SummarizerApp {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
        this.loadTheme();
    }

    initializeElements() {
        this.inputText = document.getElementById('inputText');
        this.summarizeBtn = document.getElementById('summarizeBtn');
        this.outputSection = document.getElementById('outputSection');
        this.summaryOutput = document.getElementById('summaryOutput');
        this.copyBtn = document.getElementById('copyBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.metaInfo = document.getElementById('metaInfo');
        this.continuationSteps = document.getElementById('continuationSteps');
        this.filesList = document.getElementById('filesList');
        this.autoSize = document.getElementById('autoSize');
        this.targetSentences = document.getElementById('targetSentences');
        this.targetValue = document.getElementById('targetValue');
        this.themeRadios = document.querySelectorAll('input[name="theme"]');
        this.formatRadios = document.querySelectorAll('input[name="format"]');
    }

    setupEventListeners() {
        this.summarizeBtn.addEventListener('click', () => this.summarize());
        this.copyBtn.addEventListener('click', () => this.copySummary());
        this.downloadBtn.addEventListener('click', () => this.downloadSummary());
        
        this.autoSize.addEventListener('change', () => this.toggleAutoSize());
        this.targetSentences.addEventListener('input', () => this.updateTargetValue());
        
        this.themeRadios.forEach(radio => {
            radio.addEventListener('change', () => this.setTheme(radio.value));
        });
        
        // Enable Enter key to summarize (Ctrl+Enter)
        this.inputText.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.summarize();
            }
        });
    }

    toggleAutoSize() {
        const isAuto = this.autoSize.checked;
        this.targetSentences.disabled = isAuto;
        if (isAuto) {
            this.targetSentences.style.opacity = '0.5';
        } else {
            this.targetSentences.style.opacity = '1';
        }
    }

    updateTargetValue() {
        this.targetValue.textContent = this.targetSentences.value;
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('carryon-theme') || 'light';
        this.setTheme(savedTheme);
        
        // Update radio buttons
        const themeRadio = document.querySelector(`input[name="theme"][value="${savedTheme}"]`);
        if (themeRadio) {
            themeRadio.checked = true;
        }
    }

    setTheme(theme) {
        document.body.setAttribute('data-theme', theme);
        localStorage.setItem('carryon-theme', theme);
        
        // Update radio buttons
        const themeRadio = document.querySelector(`input[name="theme"][value="${theme}"]`);
        if (themeRadio) {
            themeRadio.checked = true;
        }
    }



    async summarize() {
        const text = this.inputText.value.trim();
        if (!text) {
            alert('Please enter some text to summarize.');
            return;
        }

        const isAuto = this.autoSize.checked;
        const targetSentences = isAuto ? null : parseInt(this.targetSentences.value);

        // Show loading state
        this.summarizeBtn.disabled = true;
        this.summarizeBtn.textContent = 'Creating Summary...';
        this.outputSection.style.display = 'none';

        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    target_sentences: targetSentences
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to summarize');
            }

            const data = await response.json();
            this.displaySummary(data.summary, data.meta, text);

        } catch (error) {
            console.error('Summarization error:', error);
            alert('Error creating summary: ' + error.message);
        } finally {
            this.summarizeBtn.disabled = false;
            this.summarizeBtn.textContent = 'Create Summary';
        }
    }

    displaySummary(summary, meta, originalText) {
        // Get selected format
        const format = document.querySelector('input[name="format"]:checked').value;
        
        let displaySummary = summary;
        if (format === 'markdown') {
            // Convert to markdown format (simple conversion)
            displaySummary = summary.replace(/\n\n/g, '\n\n');
        }

        this.summaryOutput.textContent = displaySummary;
        this.metaInfo.textContent = `Words: ${meta.words_total} · Chunks: ${meta.chunks} · Target sentences: ${meta.target_sentences}`;

        // Check for file paths and show continuation steps
        const files = this.extractFilePaths(originalText);
        if (files.length > 0) {
            this.filesList.innerHTML = files.map(file => 
                `<li>Open <code>${file}</code> and apply needed changes based on the summary.</li>`
            ).join('');
            this.continuationSteps.style.display = 'block';
        } else {
            this.continuationSteps.style.display = 'none';
        }

        this.outputSection.style.display = 'block';
        this.outputSection.scrollIntoView({ behavior: 'smooth' });
    }

    extractFilePaths(text) {
        const filePattern = /\b[\w\-/\\]+\.(?:py|ts|tsx|js|json|md|txt|yaml|yml|xml|html|css|java|cpp|c|h|php|rb|go|rs|swift|kt|scala|sh|bat|ps1)\b/g;
        const matches = text.match(filePattern) || [];
        return [...new Set(matches)].sort(); // Remove duplicates and sort
    }

    async copySummary() {
        const text = this.summaryOutput.textContent;
        if (!text) {
            alert('No summary to copy.');
            return;
        }

        try {
            await navigator.clipboard.writeText(text);
            const originalText = this.copyBtn.textContent;
            this.copyBtn.textContent = '✓ Copied';
            setTimeout(() => {
                this.copyBtn.textContent = originalText;
            }, 2000);
        } catch (error) {
            console.error('Copy failed:', error);
            alert('Failed to copy to clipboard.');
        }
    }

    downloadSummary() {
        const text = this.summaryOutput.textContent;
        if (!text) {
            alert('No summary to download.');
            return;
        }

        const format = document.querySelector('input[name="format"]:checked').value;
        const extension = format === 'markdown' ? 'md' : 'txt';
        const mimeType = format === 'markdown' ? 'text/markdown' : 'text/plain';

        const blob = new Blob([text], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `summary.${extension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        URL.revokeObjectURL(url);
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SummarizerApp();
});