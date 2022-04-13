
import json
class ApiAnswer:
    def __init__(self, status: bool, data: object = '', error: str = ''):
        self.status = status
        self.data = data
        self.error = error
    def json(self):
        return json.dumps(
            self.as_dict()
        )
    def as_dict(self) -> dict:
        return {
            'status': self.status,
            'response': self.data,
            'error': self.error
        }
