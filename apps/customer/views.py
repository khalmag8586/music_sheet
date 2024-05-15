from django.http import Http404, HttpResponse  # added by me
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (
    generics,
    status,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import JSONParser

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

import uuid
import csv

from apps.customer.models import Customer
from apps.customer.serializers import CustomerSerializer

from music_sheet.pagination import StandardResultsSetPagination


class CustomerLoginView(APIView):
    # Primary login view
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        identifier = request.data.get("identifier")  # Field for email or phone number
        password = request.data.get("password")

        # Filter using Q objects to match either email or phone_number
        customer = Customer.objects.filter(
            Q(email=identifier) | Q(mobile_number=identifier)
        ).first()

        if customer is None:
            raise AuthenticationFailed(
                _("Email or phone number or password is invalid")
            )

        if not customer.is_active:
            raise AuthenticationFailed(_("User account is inactive"))
        if customer.is_deleted == True:
            raise AuthenticationFailed(_("This user is deleted"))
        if not customer.check_password(password):
            raise AuthenticationFailed(
                _("Email or phone number or password is invalid")
            )

        refresh = RefreshToken.for_user(customer)
        response = Response()

        response.data = {
            "identifier": (
                customer.email
                if customer.email == identifier
                else customer.mobile_number
            ),
            "name": customer.name,
            "is_staff": customer.is_staff,
            "is_customer": customer.is_customer,
            "access_token": str(refresh.access_token),
            # "refresh_token": str(refresh),
        }
        return response


class CreateCustomerView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    

    def perform_create(self, serializer):
        # Capitalize the user's name before saving
        name = serializer.validated_data.get("name", "")
        capitalized_name = name.title()
        serializer.save(name=capitalized_name)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"detail": _("Customer created successfully")},
            status=status.HTTP_201_CREATED,
        )


from music_sheet.custom_permissions import CustomerPermission


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.filter(is_deleted=False, is_customer=True)
    serializer_class = CustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomerPermission]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "name_ar", "mobile_number", "email"]
    ordering_fields = ["name"]
