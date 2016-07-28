# from django.shortcuts import render
from django.views.generic import DetailView

from .models import User


class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail.html"
