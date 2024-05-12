from django.urls import path

from apps.project.views import (
    ProjectCreateView,
    ProjectListView,
    DeletedProjectListView,
    ProjectRetrieveView,
    ActiveProjectListView,
    ProjectChangeActiveView,
    ProjectUpdateView,
    ProjectImagesUpdateView,
    ProjectImagesDeleteView,
    ProjectDeleteTemporaryView,
    ProjectRestoreView,
    ProjectDeleteView,ProjectDialogView,
)

app_name = "project"

urlpatterns = [
    path("project_create/", ProjectCreateView.as_view(), name="project-create"),
    path("project_list/", ProjectListView.as_view(), name="project-list"),
    path(
        "project_deleted_list/",
        DeletedProjectListView.as_view(),
        name="project-deleted-list",
    ),
    path("project_retrieve/", ProjectRetrieveView.as_view(), name="project-retrieve"),
    path("active_project/", ActiveProjectListView.as_view(), name="active-project"),
    path(
        "change_project_status/",
        ProjectChangeActiveView.as_view(),
        name="change_project_status",
    ),
    path("project_update/", ProjectUpdateView.as_view(), name="project-update"),
    path(
        "project_image_update/",
        ProjectImagesUpdateView.as_view(),
        name="project-image-update",
    ),
    path(
        "project_image_delete/",
        ProjectImagesDeleteView.as_view(),
        name="project-image-delete",
    ),
    path(
        "project_temp_delete/",
        ProjectDeleteTemporaryView.as_view(),
        name="project-temp-delete",
    ),
    path('project_restore/',ProjectRestoreView.as_view(),name='project-restore'),
    path('project_delete/',ProjectDeleteView.as_view(),name='project-delete'),
    path('Project_dialog/',ProjectDialogView.as_view(),name='project-dialog'),

]
