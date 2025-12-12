"""
CarryOn Summary - Main Flask Application
Restructured with proper backend/frontend separation
"""
from flask import Flask, send_from_directory, abort
from flask_cors import CORS
from pathlib import Path
import os

# Import route blueprints
from backend.routes.api_routes import api_bp
from backend.routes.web_routes import web_bp


def create_app(config=None):
    """
    Application factory pattern for creating Flask app
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured Flask application instance
    """
    # Create Flask app with proper template and static folders
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Enable CORS for all routes (needed for browser extension)
    CORS(app, origins=['*'])
    
    # Configuration
    app.config.update({
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
        'DEBUG': os.environ.get('FLASK_DEBUG', 'True').lower() == 'true',
        'TESTING': False,
        'JSON_SORT_KEYS': False,
        'JSONIFY_PRETTYPRINT_REGULAR': True
    })
    
    # Apply custom configuration if provided
    if config:
        app.config.update(config)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
    
    # Static file serving routes for Vercel
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        """Serve static files (CSS, JS) directly through Flask"""
        try:
            # Try to serve from the frontend static folder
            static_dir = Path(__file__).parent / '../frontend/static'
            if static_dir.exists():
                return send_from_directory(static_dir, filename)
            
            # Fallback: try root static folder
            root_static = Path(__file__).parent / '../../static'
            if root_static.exists():
                return send_from_directory(root_static, filename)
                
            abort(404)
        except Exception:
            abort(404)
    
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        """Serve asset files (images, logos) directly through Flask"""
        try:
            # Try to serve from the assets folder
            assets_dir = Path(__file__).parent / '../assets'
            if assets_dir.exists():
                return send_from_directory(assets_dir, filename)
            
            # Fallback: try root assets folder
            root_assets = Path(__file__).parent / '../../assets'
            if root_assets.exists():
                return send_from_directory(root_assets, filename)
                
            abort(404)
        except Exception:
            abort(404)
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint not found', 'code': 'NOT_FOUND'}, 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return {'error': 'Method not allowed', 'code': 'METHOD_NOT_ALLOWED'}, 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error', 'code': 'INTERNAL_ERROR'}, 500
    
    # Add some useful context processors
    @app.context_processor
    def inject_globals():
        return {
            'app_name': 'CarryOn Summary',
            'app_version': '1.0.0',
            'api_base': '/api'
        }
    
    return app


def main():
    """Main entry point for running the application"""
    app = create_app()
    
    # Get configuration from environment
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🚀 Starting CarryOn Summary Server...")
    print(f"   📍 Host: {host}")
    print(f"   🔌 Port: {port}")
    print(f"   🐛 Debug: {debug}")
    print()
    print("📱 Access points:")
    print(f"   🏠 Landing page: http://localhost:{port}/")
    print(f"   ✂️  Web app:      http://localhost:{port}/app")
    print(f"   🔧 API:          http://localhost:{port}/api/info")
    print(f"   ❤️  Health:       http://localhost:{port}/api/health")
    print()
    
    # Run the application
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()