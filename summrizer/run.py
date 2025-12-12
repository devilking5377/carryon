#!/usr/bin/env python3
"""
Simple run script for CarryOn Summary
"""
import os
import sys
import time
import webbrowser
import urllib.request
import urllib.error
from pathlib import Path

def wait_url(url, tries=15, pause=0.5):
    """Wait for URL to become available"""
    for _ in range(tries):
        try:
            with urllib.request.urlopen(url) as r:
                if r.status == 200:
                    return True
        except (urllib.error.URLError, Exception):
            time.sleep(pause)
    return False

def main():
    """Start the Flask app and open browser"""
    print("🚀 Starting CarryOn Summary...")
    print()
    
    # Check if requirements are installed
    try:
        import flask
        from flask_cors import CORS
    except ImportError:
        print("❌ Missing dependencies. Installing...")
        os.system(f"{sys.executable} -m pip install flask flask-cors")
        print("✅ Dependencies installed!")
        print()
    
    # Start the Flask app in background
    print("🌐 Starting Flask server on http://localhost:5000...")
    
    # Import and run the app
    import sys
    from pathlib import Path
    
    # Add backend to Python path
    backend_path = Path(__file__).parent / "backend"
    sys.path.insert(0, str(backend_path))
    
    from backend.main import create_app
    app = create_app()
    
    # Start server in a separate thread
    import threading
    def run_server():
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    if wait_url("http://localhost:5000/api/health"):
        print("✅ Server started successfully!")
        print()
        print("📱 Opening browser...")
        time.sleep(1)
        
        # Open only the landing page
        webbrowser.open_new_tab("http://localhost:5000/")
        
        print()
        print("🎉 CarryOn Summary is running!")
        print("   📄 Landing page: http://localhost:5000/")
        print("   ✂️  Web app:      http://localhost:5000/app")
        print("   🔧 API:          http://localhost:5000/api/summarize")
        print("   ❤️  Health:       http://localhost:5000/healthz")
        print()
        print("Press Ctrl+C to stop the server")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
    else:
        print("❌ Failed to start server")

if __name__ == "__main__":
    main()