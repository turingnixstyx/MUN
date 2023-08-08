import logging
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Create a logger instance
logger = logging.getLogger(__name__)

# Define log levels
logger.debug("This is a debug message")
logger.info("This is an informational message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")


def handle_exceptions(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            result = method(*args, **kwargs)
            logger.info("Success in %s", method.__name__)
            return result
        except Exception as e:
            logger.error("Error in %s: %s", method.__name__, e)

    return wrapper


def handle_exceptions_class(kclass):
    for attr_name in dir(kclass):
        attr = getattr(kclass, attr_name)
        if callable(attr_name):
            setattr(kclass, attr_name, handle_exceptions(attr))

    return kclass
