# from django.shortcuts import render
from django.views.generic import DetailView

from .models import Account


class AccountDetailView(DetailView):
    model = Account
    template_name = "app_accounts/account_detail.html"
