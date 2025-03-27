# This file can be left empty or used to set a default settings module
# Import the environment loader
from ..utils.env_loader import load_environment_file

# Ensure environment variables are loaded
load_environment_file()

# Optional: Set default settings module
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cpmp_project.settings.development')