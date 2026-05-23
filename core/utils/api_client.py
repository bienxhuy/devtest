import os
import requests


class APIClient:
    def __init__(self, token=None):
        self.base_url = os.getenv("BASE_URL", "http://localhost:3000")
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
            self._token = token
            self._is_authenticated = True
        else:
            self._is_authenticated = False

    # Helper methods for making requests
    def get(self, path, **kwargs):
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    def post(self, path, **kwargs):
        return self.session.post(f"{self.base_url}{path}", **kwargs)

    def delete(self, path, **kwargs):
        return self.session.delete(f"{self.base_url}{path}", **kwargs)
    
    # Token management
    def is_authenticated(self):
        return getattr(self, "_is_authenticated", False)
    
    def set_token(self, token):
        self.session.headers["Authorization"] = f"Bearer {token}"
        self._token = token
        self._is_authenticated = True
        
    def get_token(self):
        return getattr(self, "_token", None)
