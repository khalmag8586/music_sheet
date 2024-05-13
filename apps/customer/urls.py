from django.urls import path
from apps.customer.views import (
    LoginView,
    CreateCustomerView,
    CustomerListView,
)

app_name = "customer"
urlpatterns = [
    path("customer_registration/", CreateCustomerView.as_view(), name="registration"),
    path("customer_login/", LoginView.as_view(), name="customer-login"),
    path("customer_list/", CustomerListView.as_view(), name="all-customers"),
]
