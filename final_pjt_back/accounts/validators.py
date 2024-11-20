from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not any(char in "!@#$%^&*" for char in password):
            raise ValidationError("비밀번호에 최소 하나 이상의 특수문자가 포함되어야 합니다.")

    def get_help_text(self):
        return "비밀번호에 최소 하나 이상의 특수문자가 포함되어야 합니다."