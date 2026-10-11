
from django.contrib import admin

from .models import Campaign, Task


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "campaign",
        "estimated_hours",
        "actual_hours",
        "hourly_rate",
        "labour_cost",
    )
    list_filter = ("campaign",)
    search_fields = ("title",)
    readonly_fields = ("labour_cost",)
