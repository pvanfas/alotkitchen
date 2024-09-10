from users.models import CustomUser


def run():
    for i in range(1, 21):
        mobile = f"9198769876{i:02}"
        username = mobile
        password = "Test@123"
        CustomUser.objects.create_user(username=username, mobile=mobile, password=password)
        print(f"User {username} created successfully")
    print("All users created successfully")
