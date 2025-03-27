import os
from dotenv import load_dotenv

def load_environment_file():
    """
    Load the appropriate .env file based on the current environment.
    Prioritizes explicitly set DJANGO_SETTINGS_MODULE.
    """
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'cpmp_project.settings.development')
    
    if 'production' in settings_module:
        env_file = '.env.production'
    elif 'development' in settings_module:
        env_file = '.env.development'
    else:
        env_file = '.env'
    
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