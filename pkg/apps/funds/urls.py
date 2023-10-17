from django.urls import path, include

from . import views

app_name = "funds"

match_patterns = (
    [
        path("", views.RecommendationView.as_view(), name="matches"),
        path("<slug:slug>/", views.RecommendationView.as_view(), name="match"),
    ],
    "matches"
)

urlpatterns = [
    path("profile/", views.FundProfileView.as_view(), name="profile"),
    path("matches/", include(match_patterns)),
    path("<slug:slug>/", views.FundView.as_view(), name="fund"),
    path("", views.FundView.as_view(), name="funds"),
]