from django.urls import path
from apps.partner.views import (
    PartnerCreateView,
    PartnerListView,
    DeletedPartnerListView,
    PartnerActiveListView,
    PartnerRetrieveView,
    PartnerChangeActiveView,
    PartnerUpdateView,
    PartnerDeleteTemporaryView,
    PartnerRestoreView,
    PartnerDeleteView,PartnerDialogView
)

app_name = "partner"
urlpatterns = [
    path("partner_create/", PartnerCreateView.as_view(), name="partner-create"),
    path("partner_list/", PartnerListView.as_view(), name="partner-list"),
    path(
        "partner_deleted_list/",
        DeletedPartnerListView.as_view(),
        name="deleted-partner-list",
    ),
    path(
        "partner_active_list/",
        PartnerActiveListView.as_view(),
        name="partner-active-list",
    ),
    path("partner_retrieve/", PartnerRetrieveView.as_view(), name="partner-detail"),
    path(
        "partner_change_status/",
        PartnerChangeActiveView.as_view(),
        name="partner-change-status",
    ),
    path("partner_update/", PartnerUpdateView.as_view(), name="partner-update"),
    path(
        "partner_temp_delete/",
        PartnerDeleteTemporaryView.as_view(),
        name="partner-temp-delete",
    ),
    path("partner_restore/", PartnerRestoreView.as_view(), name="partner-restore"),
    path("partner_delete/", PartnerDeleteView.as_view(), name="partner-delete"),
    path("partner_dialog/", PartnerDialogView.as_view(), name="partner-dialog"),
]
