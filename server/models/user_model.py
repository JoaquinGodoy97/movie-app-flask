import re

class User:

    def __init__(self, id, username, email, password, admin_status, user_plan):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.admin_status = admin_status
        self.user_plan = user_plan
        
    @staticmethod
    def validate_password(password):
        password_check = r"^[A-Za-z0-9]{5,9}$"

        if re.match(password_check, password):
            return True
        return False
    
    @staticmethod
    def validate_user(user):
        user_check = r"^[A-Za-z0-9]{5,9}$"
        if re.match(user_check, user):
            return True
        return False
    
    def compare_password(self, password):
        return self.password == password

    def compare_user(self, user):
        return self.username == user
