from django.utils.deprecation import MiddlewareMixin
import threading
import logging

logger = logging.getLogger(__name__)
thread_local = threading.local()

class ResetDBTableMiddleware(MiddlewareMixin):
    def process_request(self, request):
        thread_local.db_table = None  # Reset at the beginning of each request
        logger.debug("db_table reset at request start")

    def process_response(self, request, response):
        # Ensure db_table is cleared after response
        if hasattr(thread_local, 'db_table'):
            logger.debug(f"Clearing db_table from thread_local: {thread_local.db_table}")
            del thread_local.db_table
        else:
            logger.debug("No db_table found in thread_local to clear.")
        return response
