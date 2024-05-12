from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from apps.partner.models import Partner
from apps.project.models import Project


class ProjectSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "name_ar"]
        allow_empty = True


class PartnerSerializer(serializers.ModelSerializer):
    created_by_user_name = serializers.CharField(
        source="created_by.name", read_only=True
    )
    created_by_user_name_ar = serializers.CharField(
        source="created_by.name_ar", read_only=True
    )
    updated_by_user_name = serializers.CharField(
        source="updated_by.name", read_only=True
    )
    updated_by_user_name_ar = serializers.CharField(
        source="updated_by.name_ar", read_only=True
    )
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    projects = ProjectSimpleSerializer(many=True, read_only=True, source='project')  # Adjust source if needed

    class Meta:
        model = Partner
        fields = [
            "id",
            "name",
            "name_ar",
            "description",
            "photo",
            "avatar",
            "created_at",
            "updated_at",
            "is_active",
            "created_by",
            "created_by_user_name",
            "created_by_user_name_ar",
            "updated_by",
            "updated_by_user_name",
            "updated_by_user_name_ar",
            "projects",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "avatar",
        ]

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d")


class PartnerDeletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ["is_deleted"]


class PartnerActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ["is_active"]


class partnerDialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ["id", "name", "name_ar"]
