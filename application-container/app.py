"""
Main function for the application.
"""
import logging
import json

def main():
    """
    Main function to configure logging and read configuration from a shared volume.
    """
    # Configure the logging module to display log messages in the console
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("Hello, Docker!")
    logger.info("Sample logger logs.")

    # Read the configuration from the shared volume
    config_file_path = '/shared-volume/config.json'
    try:
        with open(config_file_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        logger.error("Configuration file '%s' not found.", config_file_path)
        return
    except json.JSONDecodeError as json_error:
        logger.error("Error decoding JSON in configuration file: %s", json_error)
        return

    # Access configuration values
    logger.info("Configuration:")
    logger.info("Key1: %s", config.get('key1'))
    logger.info("Key2: %s", config.get('key2'))

if __name__ == "__main__":
    main()
