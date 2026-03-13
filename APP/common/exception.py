
        
import traceback


class CustomException(Exception):

    def __init__(self, message: str, error_detail: Exception = None):
        self.error_message = self.get_detailed_error_message(message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(message, error_detail):

        if error_detail:
            tb = traceback.extract_tb(error_detail.__traceback__)
            file_name, line_number, func, text = tb[-1]
        else:
            file_name = "Unknown"
            line_number = "Unknown"

        return f"{message} | Error: {error_detail} | File: {file_name} | Line: {line_number}"

    def __str__(self):
        return self.error_message