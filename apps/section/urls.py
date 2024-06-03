from django.urls import path
from apps.section.views import (
    SectionCreateView,
    SectionListView,
    SectionRetrieveView,
    SectionUpdateView,
    SectionMediaUpdateView,
    SectionMediaDeleteView,
    SectionDeleteView,
)

app_name = "section"

urlpatterns = [
    path("section_create/", SectionCreateView.as_view(), name="create-section"),
    path("section_list/", SectionListView.as_view(), name="list-section"),
    path("section_retrieve/", SectionRetrieveView.as_view(), name="retrieve-section"),
    path("section_update/", SectionUpdateView.as_view(), name="section-update"),
    path(
        "section_media_update/",
        SectionMediaUpdateView.as_view(),
        name="section_media_update",
    ),
    path(
        "section_media_delete/",
        SectionMediaDeleteView.as_view(),
        name="section_media_delete",
    ),
    path("section_delete/", SectionDeleteView.as_view(), name="delete-section"),
]
