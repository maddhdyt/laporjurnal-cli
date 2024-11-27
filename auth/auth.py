from .login import Login
from .register import Register

class Authentication:
    def __init__(self):
        self.login = Login()
        self.register = Register()
    
    def start_login(self):
        return self.login.login()
    
    def start_register(self):
        return self.register.register()