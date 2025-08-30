import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with a standard configuration.
    
    Args:
        name (str): The name of the logger (usually __name__ of the module)
        
    Returns:
        Logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
