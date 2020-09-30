import sys
import traceback
import logging
import datetime

from importlib import import_module


def enable_traceback(original_function):
    
    logger = logging.getLogger(datetime.datetime.now().strftime('%d/%m/%Y'))
    
    def wrapper(*args, **kwargs):
        
        try:
            return original_function(*args, **kwargs)
        
        except Exception as e:
            
            if isinstance(args[0], import_module('abstract.viewsets').CreateListRetrieveUpdateViewSet):
                request = args[1]
                
            else:
                request = args[0]
            
            type_ = sys.exc_info()[0].__name__
            tb = traceback.format_exc()
            print(tb)
            logger.error(f'Type: { type_ }, Details: { tb }')
            traceback.print_exc()
    
    return wrapper
