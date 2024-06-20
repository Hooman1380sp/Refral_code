from django.contrib.auth.models import BaseUserManager as BUM


class UserManager(BUM):
    def create_user(self, referral_code, password, email: str):
        user = self.model(email=self.normalize_email(email), referral_code=referral_code)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, referral_code: str, password, email: str):
        user = self.create_user(email=self.normalize_email(email), password=password, referral_code=referral_code)
        user.is_admin = True
        user.save()
        return user
