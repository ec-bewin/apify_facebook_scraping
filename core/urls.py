from django.contrib import admin
from django.urls import path
from core.views import FetchGroupDataView, APifyWebhookView

urlpatterns = [
    path(
        "facebook_data_upload/", FetchGroupDataView.as_view(), name="fetch_group_data"
    ),
    path("apify_webhook/", APifyWebhookView.as_view(), name="apify_webhook"),
]
