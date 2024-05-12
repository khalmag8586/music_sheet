from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import (
    generics,
    status,
)

from rest_framework_simplejwt.authentication import JWTAuthentication

from music_sheet.pagination import StandardResultsSetPagination

from apps.project.models import Project, ProjectImages
from apps.project.serializers import (
    ProjectSerializer,
    ProjectImageSerializer,
    ProjectDialogSerializer,
    ProjectActiveSerializer,
    ProjectDeleteSerializer,
)


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.action = self.request.method.lower()

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
            {"detail": _("Project created successfully")},
            status=status.HTTP_201_CREATED,
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectSerializer
        elif self.action == "upload_image":
            return ProjectImageSerializer

        return self.serializer_class

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "name",
        "name_ar",
    ]
    ordering_fields = ["name", "-name", "name_ar", "-name_ar"]


class DeletedProjectListView(generics.ListAPIView):
    queryset = Project.objects.filter(is_deleted=True)
    serializer_class = ProjectSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "name_ar"]
    ordering_fields = ["name", "-name", "name_ar", "-name_ar"]


class ProjectRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        project_id = self.request.query_params.get("project_id")
        project = get_object_or_404(Project, id=project_id)
        return project


class ActiveProjectListView(generics.ListAPIView):
    queryset = Project.objects.filter(is_deleted=False, is_active=True)
    serializer_class = ProjectSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "name_ar"]
    ordering_fields = ["name", "-name", "name_ar", "-name_ar"]


class ProjectChangeActiveView(generics.UpdateAPIView):
    serializer_class = ProjectActiveSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        project_ids = request.data.get("project_id", [])
        partial = kwargs.pop("partial", False)
        is_active = request.data.get("is_active")
        if is_active is None:
            return Response(
                {"detail": _("'is_active' field is required")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for project_id in project_ids:
            instance = get_object_or_404(Project, id=project_id)
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return Response(
            {"detail": _("Project status changed successfully")},
            status=status.HTTP_200_OK,
        )


class ProjectUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        project_id = self.request.query_params.get("project_id")
        project = get_object_or_404(Project, id=project_id)
        return project

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": _("Project Updated successfully")}, status=status.HTTP_200_OK
        )


class ProjectImagesUpdateView(generics.UpdateAPIView):
    serializer_class = ProjectImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProjectImages.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def patch(self, request, *args, **kwargs):
        image_id = request.data.get(
            "image_id"
        )  # Get the image ID from the request body
        if not image_id:
            return Response(
                {"detail": _("Image ID is required.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            instance = self.get_queryset().get(id=image_id)
        except ProjectImages.DoesNotExist:
            return Response(
                {"detail": _("Image not found.")}, status=status.HTTP_404_NOT_FOUND
            )

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # return Response(serializer.data)
        return Response(
            {"detail": _("Project image updated successfully")},
            status=status.HTTP_200_OK,
        )


class ProjectImagesDeleteView(generics.DestroyAPIView):
    serializer_class = ProjectImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProjectImages.objects.all()

    def delete(self, request, *args, **kwargs):
        image_ids = request.data.get("image_id", [])
        for image_id in image_ids:
            instance = get_object_or_404(ProjectImages, id=image_id)
            instance.delete()
        return Response(
            {"detail": _("Project image deleted successfully")},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProjectDeleteTemporaryView(generics.UpdateAPIView):
    serializer_class = ProjectDeleteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        project_ids = request.data.get("project_id", [])
        partial = kwargs.pop("partial", False)
        is_deleted = request.data.get("is_deleted")

        if is_deleted == False:
            return Response(
                {"detail": _("These projects are not deleted")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for project_id in project_ids:
            instance = get_object_or_404(Project, id=project_id)
            if instance.is_deleted:
                return Response(
                    {
                        "detail": _(
                            "Project with ID {} is already temp deleted".format(
                                project_id
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
            {"detail": _("Projects temp deleted successfully")},
            status=status.HTTP_200_OK,
        )


class ProjectRestoreView(generics.RetrieveUpdateAPIView):

    serializer_class = ProjectDeleteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        project_ids = request.data.get("project_id", [])
        partial = kwargs.pop("partial", False)
        is_deleted = request.data.get("is_deleted")

        if is_deleted == True:
            return Response(
                {"detail": _("Projects are already deleted")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for project_id in project_ids:
            instance = get_object_or_404(Project, id=project_id)
            if instance.is_deleted == False:
                return Response(
                    {
                        "detail": _(
                            "Projects with ID {} is not deleted".format(project_id)
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
            {"detail": _("Projects restored successfully")}, status=status.HTTP_200_OK
        )


class ProjectDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        project_ids = request.data.get("project_id", [])
        for project_id in project_ids:
            instance = get_object_or_404(Project, id=project_id)
            instance.delete()

        return Response(
            {"detail": _("Project permanently deleted successfully")},
            status=status.HTTP_204_NO_CONTENT,
        )


# Project Dialogs
class ProjectDialogView(generics.ListAPIView):
    serializer_class = ProjectDialogSerializer
    queryset = Project.objects.filter(is_deleted=False, is_active=True)
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
