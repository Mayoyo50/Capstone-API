#!/usr/bin/env python3

import os
import secrets
import argparse

class EnvironmentGenerator:
    @staticmethod
    def generate_secret_key(length=50):
        """Generate a secure random secret key."""
        return secrets.token_urlsafe(length)

    def generate_env_file(self, env_type='development', output_dir=None):
        """Generate environment-specific .env file."""
        # Generate actual values
        secret_key = self.generate_secret_key()
        jwt_secret_key = self.generate_secret_key()
        db_password = secrets.token_urlsafe(16)

        # Database configuration
        db_name = 'defaultdb'
        db_user = 'avnadmin'
        db_host = 'capstone-capstone-33.c.aivencloud.com'
        db_port = '11911'

        # Construct DATABASE_URL
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        # Environment configurations
        env_config = {
            # Core Django settings
            'SECRET_KEY': secret_key,
            'JWT_SECRET_KEY': jwt_secret_key,
            'DEBUG': 'False' if env_type == 'production' else 'True',
            'ENV_TYPE': 'development' if env_type == 'development' else 'production',
            'DJANGO_SETTINGS_MODULE': f'cpmp_project.settings.{env_type}',
            
            # Database configuration
            'DATABASE_URL': database_url,  # Add DATABASE_URL here
            'AIVEN_DB_NAME': db_name,
            'AIVEN_DB_USER': db_user,
            'AIVEN_DB_PASSWORD': db_password,
            'AIVEN_DB_HOST': db_host,
            'AIVEN_DB_PORT': db_port,
            
            # Additional production settings
            'RENDER_HOSTNAME': 'your-app-name.onrender.com',
            'FRONTEND_URL': 'https://your-production-domain.com',
        }

        # Determine output path
        if output_dir is None:
            output_dir = os.getcwd()
        
        filepath = os.path.join(output_dir, f'.env.{env_type}')

        # Write environment file
        with open(filepath, 'w') as f:
            for key, value in env_config.items():
                f.write(f"{key}={value}\n")
        
        # Print out the generated values (except for very sensitive keys)
        print("Generated Environment Configuration:")
        for key, value in env_config.items():
            # Only partially hide extremely sensitive keys
            if key in ['SECRET_KEY', 'JWT_SECRET_KEY', 'DATABASE_URL']:
                print(f"{key}={value[:10]}... (truncated)")
            else:
                print(f"{key}={value}")
        
        print(f"\nEnvironment file saved to: {filepath}")
        
        return env_config

def main():
    parser = argparse.ArgumentParser(description='Generate Environment Configuration Files')
    parser.add_argument(
        '--type', 
        choices=['development', 'production'], 
        default='development', 
        help='Type of environment to generate'
    )
    parser.add_argument(
        '--output', 
        help='Output directory for env file (default: current directory)'
    )
    
    args = parser.parse_args()

    generator = EnvironmentGenerator()
    generator.generate_env_file(
        env_type=args.type, 
        output_dir=args.output
    )

if __name__ == '__main__':
    main()

# # Generate development environment file
# python scripts/generate_env.py --type development

# # Generate production environment file
# python scripts/generate_env.py --type production

# # Specify custom output directory
# python scripts/generate_env.py --type development --output /path/to/output