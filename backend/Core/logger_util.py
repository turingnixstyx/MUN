import logging
from functools import wraps

class MUNLogger():
    def __init__(self) -> None:
        self.debug = "*********************************"

        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )

        # Create a logger instance
        self.logger = logging.getLogger(__name__)

        # Define log levels
        self.logger.debug("This is a debug message")
        self.logger.info("This is an informational message")
        self.logger.warning("This is a warning message")
        self.logger.error("This is an error message")
        self.logger.critical("This is a critical message")


    


    def handle_exceptions_class(self, kclass):
        print("reaching inside try block class" + self.debug)
        for attr_name in dir(kclass):
            print(attr_name)
            attr = getattr(kclass, attr_name)
            if callable(attr) and not attr_name.startswith("__"):
                print("Sucessfully selecting funtion", attr_name, self.debug)
                setattr(kclass, attr_name, self.handle_exceptions(attr))

        return kclass
    


    def handle_exceptions(self, method):
        print("reaching inside handle exception", self.debug)
        @wraps(method)
        def wrapper(*args, **kwargs):
            try:
                print("Reaching Inside Try Block", self.debug)
                result = method(*args, **kwargs)
                self.logger.info("Success in %s", method.__name__)
                print("Sucess in %s ", method.__name__,self.debug)
                return result
            except Exception as e:
                self.logger.error("Error in %s: %s", method.__name__, e)

        return wrapper