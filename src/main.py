"""
#####################################
# Run the application from here     #
# Avoid to mix start/function calls #
#####################################
"""
from src.app import create_app
from src.app.logger import setup_logger

# Gather Logs throughout programm
logger = setup_logger()
# Set file as main/startpoint
if __name__ == '__main__':
    # Verify that app has started
    logger.info("APP STARTED")
    # Get Flask app from factory to start
    create_app().run(debug=True)