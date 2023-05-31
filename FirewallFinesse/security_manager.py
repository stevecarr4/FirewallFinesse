import cgi

class SecurityManager:
    @staticmethod
    def escape_html(input_string):
        """
        Escapes HTML special characters in a string.
        """
        return cgi.escape(input_string)
