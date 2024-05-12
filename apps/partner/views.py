from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from rest_framework import (
    generics,
    status,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from apps.partner.models import Partner
from apps.partner.serializers import (
    PartnerSerializer,
    PartnerActiveSerializer,
    PartnerDeletedSerializer,
    partnerDialogSerializer,
)

from music_sheet.pagination import StandardResultsSetPagination


class PartnerCreateView(generics.CreateAPIView):
    serializer_class = PartnerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"detail": _("Partner created successfully")},
            status=status.HTTP_201_CREATED,
        )


class PartnerListView(generics.ListAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.filter(is_deleted=False)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "name_ar"]
    ordering_fields = ["name", "-name", "name_ar", "-name_ar"]


class DeletedPartnerListView(generics.ListAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.filter(is_deleted=True)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "name_ar"]
    ordering_fields = ["name", "-name", "name_ar", "-name_ar"]


class PartnerActiveListView(generics.ListAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.filter(is_deleted=False, is_active=True)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "name_ar"]
    ordering_fields = ["name", "-name", "name_ar", "-name_ar"]


class PartnerRetrieveView(generics.RetrieveAPIView):
    serializer_class = PartnerSerializer
    lookup_field = "id"

    def get_object(self):
        partner_id = self.request.query_params.get("partner_id")
        partner = get_object_or_404(Partner, id=partner_id)
        return partner


class PartnerChangeActiveView(generics.UpdateAPIView):
    serializer_class = PartnerActiveSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partner_ids = request.data.get("partner_id", [])
        partial = kwargs.pop("partial", False)
        is_active = request.data.get("is_active")
        if is_active is None:
            return Response(
                {"detail": _("'is_active' field is required")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for partner_id in partner_ids:
            instance = get_object_or_404(Partner, id=partner_id)
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return Response(
            {"detail": _("Partner status changed successfully")},
            status=status.HTTP_200_OK,
        )


class PartnerUpdateView(generics.UpdateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    lookup_field = "id"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        partner_id = self.request.query_params.get("partner_id")
        partner = get_object_or_404(Partner, id=partner_id)
        return partner

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": _("Partner updated successfully")}, status=status.HTTP_200_OK
        )


class PartnerDeleteTemporaryView(generics.UpdateAPIView):
    serializer_class = PartnerDeletedSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partner_ids = request.data.get("partner_id", [])
        partial = kwargs.pop("partial", False)
        is_deleted = request.data.get("is_deleted")

        if is_deleted == False:
            return Response(
                {"detail": _("These partners are not deleted")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for partner_id in partner_ids:
            instance = get_object_or_404(Partner, id=partner_id)
            if instance.is_deleted:
                return Response(
                    {
                        "detail": _(
                            "Partner with ID {} is already temp deleted".format(
                                partner_id
                            )
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            instance.is_active = False
            instance.save()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        return Response(
            {"detail": _("Partner temp deleted successfully")},
            status=status.HTTP_200_OK,
        )


class PartnerRestoreView(generics.RetrieveUpdateAPIView):

    serializer_class = PartnerDeletedSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partner_ids = request.data.get("partner_id", [])
        partial = kwargs.pop("partial", False)
        is_deleted = request.data.get("is_deleted")

        if is_deleted == True:
            return Response(
                {"detail": _("Partners are already deleted")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for partner_id in partner_ids:
            instance = get_object_or_404(Partner, id=partner_id)
            if instance.is_deleted == False:
                return Response(
                    {
                        "detail": _(
                            "Partner with ID {} is not deleted".format(partner_id)
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            instance.is_active = True

            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        return Response(
            {"detail": _("Partner restored successfully")}, status=status.HTTP_200_OK
        )


class PartnerDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        partner_ids = request.data.get("partner_id", [])
        for partner_id in partner_ids:
            instance = get_object_or_404(Partner, id=partner_id)
            instance.delete()

        return Response(
            {"detail": _("Partner permanently deleted successfully")},
            status=status.HTTP_204_NO_CONTENT,
        )


class PartnerDialogView(generics.ListAPIView):
    queryset = Partner.objects.filter(is_deleted=False)
    serializer_class = partnerDialogSerializer
