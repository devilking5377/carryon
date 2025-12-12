# CarryOn Summary

Concise, paste-ready summaries for long AI outputs. Single Flask server with integrated web UI, API, and browser extension support.

## Features
- Auto-size summaries based on input length, or set a target sentence count
- Preserves lists, dates, names, bullet points, and step-by-step details
- Detects file-like paths and shows continuation steps
- Modern web UI with light/dark theme support
- Flask API endpoint for integrations
- Browser extension to summarize selected content on any page

## Architecture
- **Single Flask Server**: All-in-one solution with web UI, API, and static file serving
- **API**: `POST /api/summarize` endpoint
- **Web UI**: Modern HTML/CSS/JS interface (replaces Streamlit)
- **Summarizer**: Extractive scoring and chunking algorithm
- **Extension**: MV3 browser extension with auto-detection
- **Landing**: Integrated documentation and download page

## Quick Start

### Option 1: Simple Run Script
```bash
cd summrizer
python run.py
```
This will automatically install dependencies and open your browser.

### Option 2: Manual Setup
```bash
cd summrizer
pip install flask flask-cors
python app.py
```

### Access Points
- **Landing page**: http://localhost:5000/
- **Web App**: http://localhost:5000/app
- **API**: http://localhost:5000/api/summarize
- **Health Check**: http://localhost:5000/healthz

## Web UI Features
- **Theme Toggle**: Light/Dark mode with automatic logo switching
- **Auto-size**: Automatically determines optimal summary length
- **Manual Control**: Set target sentence count (4-80)
- **Output Formats**: Plain text or Markdown
- **Download**: Save summaries as .txt or .md files
- **Continuation Steps**: Automatically detects file paths and suggests next steps
- **Responsive Design**: Works on desktop and mobile

## Browser Extension (Chromium)
1. **Download**: Click "Download Extension" on the landing page
2. **Install**: 
   - Go to `chrome://extensions`
   - Enable Developer Mode
   - Click "Load unpacked" and select the extracted folder
3. **Configure**: 
   - Click the extension icon
   - Set API Base URL to `http://localhost:5000`
   - Save settings
4. **Use**:
   - Select text on any page
   - Click "Grab Selection" in the popup
   - Click "Create Summary"
   - Copy or download the result

### Supported Sites
Auto-detection works on ChatGPT, Claude, Gemini, Copilot, Poe, Perplexity, and other AI chat interfaces.

### ⚠️ Important: Server Dependency
The browser extension **requires the Flask server to be running** to function. It cannot work independently. Always ensure the server is running (`python run.py`) before using the extension.

## API Reference

### POST /api/summarize
```json
// Request
{
  "text": "Your long text here...",
  "target_sentences": 16  // optional, null for auto-size
}

// Response
{
  "summary": "Concise summary here...",
  "meta": {
    "words_total": 1234,
    "chunks": 2,
    "target_sentences": 16
  }
}
```

### Other Endpoints
- `GET /` - Landing page
- `GET /app` - Web application
- `GET /healthz` - Health check
- `GET /download-extension` - Download extension ZIP

## Deployment

### Local Development
The Flask app runs in debug mode by default. For production:

```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

### Cloud Deployment
Deploy to any Flask-compatible platform:
- **Heroku**: Add `Procfile` with `web: python app.py`
- **Railway**: Automatic detection
- **Render**: Set build command to `pip install -r requirements.txt`
- **Fly.io**: Use provided Dockerfile or buildpacks

### Extension Configuration
Update the extension's API Base URL to point to your deployed server (use HTTPS for production).

## File Structure
```
summrizer/
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── run.py                   # Simple startup script
├── backend/                 # Backend logic
│   ├── main.py             # Flask application factory
│   ├── routes/             # Route blueprints
│   │   ├── api_routes.py   # API endpoints
│   │   └── web_routes.py   # Web pages
│   ├── services/           # Business logic
│   │   └── summarizer_service.py  # Text summarization
│   └── utils/              # Utility functions
│       └── file_utils.py   # File path detection
├── frontend/               # Frontend assets
│   ├── templates/          # HTML templates
│   │   ├── landing.html    # Landing page
│   │   ├── summarizer.html # Main app UI
│   │   ├── docs.html       # API documentation
│   │   ├── about.html      # About page
│   │   └── error.html      # Error pages
│   └── static/             # CSS and JavaScript
│       ├── landing.css     # Landing page styles
│       ├── landing.js      # Landing page scripts
│       ├── summarizer.css  # App styles
│       └── summarizer.js   # App functionality
└── assets/                 # Logo images
    ├── light-theme-logo.jpeg
    └── dark-theme-logo.jpeg
```

## Development

### Adding Features
- **Templates**: Edit HTML files in `frontend/templates/`
- **Styling**: Modify CSS files in `frontend/static/`
- **Frontend Logic**: Update JavaScript files in `frontend/static/`
- **API Routes**: Extend `backend/routes/api_routes.py`
- **Web Routes**: Extend `backend/routes/web_routes.py`
- **Business Logic**: Modify `backend/services/summarizer_service.py`
- **Utilities**: Add functions to `backend/utils/`

### Theme System
The app supports automatic light/dark mode detection and manual toggle:
- CSS variables in `:root` and `[data-theme="dark"]`
- JavaScript theme persistence in localStorage
- Automatic logo switching based on theme

## Privacy & Security
- **No External APIs**: Runs entirely on your infrastructure
- **No Data Collection**: Text processing happens locally
- **CORS Enabled**: Supports cross-origin requests for extension
- **No Authentication**: Suitable for personal/internal use

## Troubleshooting

### Common Issues
- **Import Error**: Make sure you're in the `summrizer` directory
- **Port Conflict**: Change port in `app.py` if 5000 is in use
- **Extension Error**: Verify API Base URL and server status
- **CORS Issues**: Flask-CORS is included for cross-origin support

### Browser Extension
- **Auto-detection not working**: Check if the site is supported
- **API connection failed**: Verify server is running and URL is correct
- **Settings not saving**: Check browser's storage permissions
- **Extension not working**: The extension requires the Flask server to be running - it cannot work independently