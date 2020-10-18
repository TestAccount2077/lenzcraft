from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password


class UserValidator(object):
    
    @staticmethod
    def validate_email(email):
        
        try:
            validate_email(email)
            return True
            
        except:
            return False
        
    @staticmethod
    def validate_password(user, password, password_confirmation):
        
        if password != password_confirmation:
            return "Passwords don't match"
            
        try:
            validate_password(password, user)
        
        except Exception as e:
            return list(e)[0]
            
