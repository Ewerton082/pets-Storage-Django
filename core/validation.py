from django.contrib.auth.models import User

def superuser_required(user):
    return user.is_superuser
