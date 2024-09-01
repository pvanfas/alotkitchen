from uuid import uuid4

from users.models import CustomUser


def run():
    for user in CustomUser.objects.all():
        user.enc_key = uuid4()
        user.save()
        print(f"User {user.username} updated")
