from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard_view"),
    # District
    path("districts/", views.DistrictListView.as_view(), name="district_list"),
    path("districts/create/", views.DistrictCreateView.as_view(), name="district_create"),
    path("districts/detail/<str:pk>/", views.DistrictDetailView.as_view(), name="district_detail"),
    path("districts/update/<str:pk>/", views.DistrictUpdateView.as_view(), name="district_update"),
    path("districts/delete/<str:pk>/", views.DistrictDeleteView.as_view(), name="district_delete"),
    # Branch
    path("branches/", views.BranchListView.as_view(), name="branch_list"),
    path("branches/create/", views.BranchCreateView.as_view(), name="branch_create"),
    path("branches/detail/<str:pk>/", views.BranchDetailView.as_view(), name="branch_detail"),
    path("branches/update/<str:pk>/", views.BranchUpdateView.as_view(), name="branch_update"),
    path("branches/delete/<str:pk>/", views.BranchDeleteView.as_view(), name="branch_delete"),
]
