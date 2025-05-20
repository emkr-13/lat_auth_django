import os
from django.core.management.commands.runserver import Command as RunserverCommand
from loguru import logger
from core.logger import logger  # Import configured logger

class Command(RunserverCommand):
    help = 'Runs the server with environment variables'

    def handle(self, *args, **options):
        port = os.getenv('APP_PORT', '3080')
        options['addrport'] = f'127.0.0.1:{port}'
        
        logger.info(f"Starting server on http://localhost:{port}")
        logger.info(f"Database: {os.getenv('DB_NAME')} on {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
        logger.info(f"Debug mode: {os.getenv('DEBUG', 'True')}")
        
        super().handle(*args, **options) 