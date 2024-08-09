from main.base import BaseTable

from .models import CustomUser as User


class UserTable(BaseTable):
    class Meta:
        model = User
        fields = ("fullname", "date_joined")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012
