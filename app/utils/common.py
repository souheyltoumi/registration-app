import random
import logging
from dao.conf.model_settings import get_settings
from fastapi import HTTPException

logger_instance = None

def generate_4_digit_code():
    """
    Generate a random 4-digit code and return it as a string.
    """
    # Generate a random 4-digit number between 1000 and 9999 (inclusive)
    code = random.randint(1000, 9999)
    
    # Convert the code to a string
    code_str = str(code)
    
    return code_str

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str, headers=None):
        super().__init__(status_code, detail, headers)
    
    def __str__(self):
        return f"{self.status_code} - {self.detail}"

class AppLogger():

    """
    Only log debug level message to the console
    """
    @staticmethod
    def log(msg: str, level="debug"):
        # Create logger
        logger = logging.getLogger("app")
        
        # Set the logging level
        logger.setLevel(logging.DEBUG)
        
        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Add formatter to ch
        ch.setFormatter(formatter)
        
        # Add ch to logger
        logger.addHandler(ch)
    
        if level == 'debug':
            logger.debug(msg=msg)
        elif level == 'warning':
            logger.warning(msg=msg)
