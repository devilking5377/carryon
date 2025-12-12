import sys
import os
from pathlib import Path

# Get the root directory
root_dir = Path(__file__).parent.parent
summrizer_dir = root_dir / 'summrizer'

# Add the summrizer directory to the Python path
sys.path.insert(0, str(summrizer_dir))

# Change working directory to summrizer for relative imports
os.chdir(str(summrizer_dir))

from backend.main import create_app

# Create the Flask app
app = create_app()

# Configure for production
app.config['DEBUG'] = False

# Vercel expects the app to be available as 'app'
if __name__ == "__main__":
    app.run(debug=False)