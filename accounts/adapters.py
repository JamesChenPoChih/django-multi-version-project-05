from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just before a social user is logged in.
        We override this to handle both existing and new users,
        bypassing the default allauth flow to integrate with our custom user system.
        """
        # The sociallogin object contains user data from the social provider.
        user_email = sociallogin.user.email
        if not user_email:
            # If for some reason we don't get an email, we can't proceed.
            # You might want to handle this case more gracefully.
            return

        try:
            # Case 1: An existing user is logging in. (改用 Django 內建 User 模型)
            user = User.objects.get(email=user_email)
            print(f"[MySocialAccountAdapter] Existing user found: {user.email}")
            
            request.session['loginFlag'] = True
            request.session['username'] = user.username

        except User.DoesNotExist:
            # Case 2: A new user is signing up. (改用 Django 內建 User 模型)
            print(f"[MySocialAccountAdapter] New user. Creating profile for: {user_email}")
            
            username = sociallogin.user.get_full_name() or user_email.split('@')[0]
            user = User.objects.create(
                email=user_email,
                username=user_email  # Django 的 username 必須唯一，這裡存入 email 避免重複
            )
            request.session['loginFlag'] = True
            request.session['username'] = username

        # In both cases, we have handled the login manually.
        # We raise ImmediateHttpResponse to stop allauth's default processing
        # and redirect the user to the homepage.
        print("[MySocialAccountAdapter] Login handled. Redirecting to /")
        raise ImmediateHttpResponse(redirect('/'))
