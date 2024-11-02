import traceback

class ErrorHandler:
    class ScrapingException(Exception):
        """Custom exception class for scraping errors."""
        def __init__(self, message):
            super().__init__(message)

    @staticmethod
    def generate_error_page(exception):
        """
        Generates an HTML page displaying the traceback of an exception.
        
        Args:
            exception (Exception): The exception to display.

        Returns:
            str: An HTML string representing the error page.
        """
        tb_str = traceback.format_exception(type(exception), exception, exception.__traceback__)
        formatted_traceback = ''.join(tb_str).replace('<', '&lt;').replace('>', '&gt;')  # HTML-safe text

        error_page = f"""
        <html>
        <body>
            <h2>An error occurred:</h2>
            <pre style="font-size:22px; font-weight:600;">{formatted_traceback}</pre>
        </body>
        </html>
        """
        return error_page
