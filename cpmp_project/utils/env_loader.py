import os
from dotenv import load_dotenv

def load_environment_file():
    """
    Load the appropriate .env file based on the current environment.
    Only loads .env files in development, skips in production.
    """
    # Skip in production (Render sets RENDER environment variable)
    if os.environ.get('RENDER') or os.environ.get('PYTHON_ENV') == 'production':
        return
    else:
        env_file = '.env.development'
    
    # Find the project root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(base_dir, env_file)
    
    # Load the environment file if it exists
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)
    else:
        print(f"Warning: {env_file} not found")

# Automatically load environment when this module is imported
load_environment_file()