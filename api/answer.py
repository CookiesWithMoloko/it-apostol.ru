from typing import Union
import json
class ApiAnswer:
    def __init__(self, status: bool, data: Union[str, list, dict] = '', error: Exception = None):
        self.status = status
        self.data = data
        self.error = error
    def throw(self) -> None:
        if self.error is not None:
            raise self.error
    def json(self) -> str:
        return json.dumps(
            self.as_dict()
        )
    def as_dict(self) -> dict:
        return {
            'status': self.status,
            'response': self.data,
            'error': str(self.error)
        }
