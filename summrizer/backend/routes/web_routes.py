"""
Web Routes for CarryOn Summary
Handles all web pages and static content serving
"""
from flask import Blueprint, render_template, send_from_directory, redirect, send_file
import os
import io
import zipfile
from pathlib import Path

# Create web blueprint
web_bp = Blueprint('web', __name__)

# Configuration paths
BASE_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"
EXT_DIR = BASE_DIR.parent / "carryon-extension"
# LANDING_DIR removed - now using templates


@web_bp.route('/')
def index():
    """Landing page - main entry point"""
    return render_template('landing.html')


@web_bp.route('/app')
def summarizer_app():
    """Main summarizer web application"""
    return render_template('summarizer.html')


@web_bp.route('/docs')
def documentation():
    """Documentation page"""
    return render_template('docs.html')


@web_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


# Asset serving routes
@web_bp.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve asset files (logos, images, etc.)"""
    if ASSETS_DIR.exists():
        return send_from_directory(str(ASSETS_DIR), filename)
    return "Asset not found", 404


# Extension serving routes
@web_bp.route('/extension/<path:filename>')
def serve_extension(filename):
    """Serve browser extension files"""
    if EXT_DIR.exists():
        return send_from_directory(str(EXT_DIR), filename)
    return "Extension file not found", 404


@web_bp.route('/download-extension')
def download_extension():
    """Download browser extension as ZIP file"""
    if not EXT_DIR.exists():
        return "Extension not found", 404
    
    try:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(EXT_DIR):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(EXT_DIR)
                    arc_path = Path("carryon-extension") / rel_path
                    z.write(str(file_path), str(arc_path))
        
        buf.seek(0)
        return send_file(
            buf,
            as_attachment=True,
            download_name="carryon-extension.zip",
            mimetype="application/zip"
        )
    except Exception as e:
        return f"Error creating extension ZIP: {str(e)}", 500


# Compatibility routes
@web_bp.route('/open/ui')
def open_ui():
    """Redirect to main app (compatibility)"""
    return redirect('/app')


@web_bp.route('/open/api')
def open_api():
    """Redirect to API info"""
    return redirect('/api/info')


@web_bp.route('/site')
def site_root():
    """Serve landing page at /site for compatibility"""
    return redirect('/')


@web_bp.route('/site/<path:path>')
def site_files(path):
    """Serve landing page files for compatibility - redirect to main pages"""
    if path == "":
        return redirect('/')
    
    # Redirect common paths to new structure
    if path in ['app.js', 'styles.css']:
        return redirect(f'/static/landing.{path.split(".")[-1]}')
    
    return redirect('/')


# Health check route (also available outside API)
@web_bp.route('/healthz')
def health_check():
    """Health check endpoint (compatibility)"""
    return {
        'ok': True,
        'status': 'healthy',
        'service': 'CarryOn Summary'
    }


# Error handlers
@web_bp.errorhandler(404)
def not_found(error):
    """Custom 404 page"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404


@web_bp.errorhandler(500)
def internal_error(error):
    """Custom 500 page"""
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500