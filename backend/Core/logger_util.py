import logging
import traceback
from functools import wraps


class MUNLogger:
    def __init__(self, name) -> None:
        self.debug = "*********************************"

        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )

        # Create a logger instance
        self.logger = logging.getLogger(name)

    def handle_exceptions_class(self, kclass):
        for attr_name in dir(kclass):
            attr = getattr(kclass, attr_name)
            if callable(attr) and not attr_name.startswith("__"):
                setattr(kclass, attr_name, self.handle_exceptions(attr))

        return kclass

    def handle_exceptions(self, method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            try:
                result = method(*args, **kwargs)
                self.logger.info("Success in %s", method.__name__)
                # print("Sucess in %s ", method.__name__, self.debug)
                return result
            except Exception as e:
                traceback.print_exc()
                self.logger.error("Error in %s: %s", method.__name__, e)

        return wrapper
