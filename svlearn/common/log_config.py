
import logging
from rich.logging import RichHandler
import sys
from pathlib import Path
from svlearn.common import singleton




@singleton
class LogConfiguration:
    """
    This class is used to configure the logging for the application.
    """
    # ---------------------------------------------------------------------------------------------
    __DEFAULT_APPLICATION_NAME: str = 'PROMPTLY'
    __DEFAULT_LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # ---------------------------------------------------------------------------------------------
    
    def __init__(self,
                 application_name = __DEFAULT_APPLICATION_NAME, 
                 with_console_logging: bool = True,
                 with_file_logging: bool = False,
                 log_file_path: str = None,
                 log_format:str = __DEFAULT_LOG_FORMAT) -> None:
        
        # Preconditions check
        if not application_name:
            raise ValueError('Must provide a non-empty value for "application_name" parameter.')

        if not log_format:
            raise ValueError('Must provide a non-empty and valid format value for "log_format" parameter.')

        if with_file_logging and not log_file_path:
            raise ValueError('Must provide a non-empty value for "log_file_path" '
            'parameter when "with_file_logging" is set to True.')
      
        if with_file_logging:
            path: Path = Path(log_file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)


        self.application_name = application_name
        self.with_console_logging = with_console_logging
        self.with_file_logging = with_file_logging
        self.log_file_path = log_file_path
        self.log_format = log_format
        self.setup_logging()

    # ---------------------------------------------------------------------------------------------
    def setup_logging(self, level: int =logging.INFO):
        """
        Set up the logging configuration.
        
        Parameters:
        - level: The logging level you want to set for the application.
        """
         
        # Create a logger object
        logger = logging.getLogger(self.application_name)
        logger.setLevel(level)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter(self.log_format)

        # Create Console log handler
        if self.with_console_logging:
            console_handler = RichHandler() #logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # Create File log handler
        if self.with_file_logging:
            file_handler = logging.FileHandler(self.log_file_path)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # Finally, we always want the RichHandler in place.
        logger.addHandler(RichHandler())
        
        # We want to log uncaught exceptions as well
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                # Call the default KeyboardInterrupt handler
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logger.error('\n' + '-'*80 +'\nUNCAUGHT EXCEPTION\n' + '-'*80, 
                            exc_info=(exc_type, exc_value, exc_traceback))
        sys.excepthook = handle_exception      

    # ---------------------------------------------------------------------------------------------

    def set_level(self, level: int = logging.INFO):
        """
        Set the logging level for the logger.
        """
        logger = logging.getLogger(self.application_name)
        logger.setLevel(level)
        
# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    """
    The main function of the application.
    """
    # Setup logging with the desired level
    log_config = LogConfiguration(with_console_logging=True, 
                                    with_file_logging=True,
                                    log_file_path='logs/promptly.log')
    log_config.set_level()

    # Now you can use the logger within your main application
    logger = logging.getLogger('THE PROMPTLY IS READY NOW!')
    logger.info("Application is starting...")



    # ... verify it can catch an uncaught exception ...
    raise ValueError("This is a test exception")

