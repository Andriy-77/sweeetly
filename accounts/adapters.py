from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.first_name = data.get("first_name", "")
        user.last_name = data.get("last_name", "")
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        return True
