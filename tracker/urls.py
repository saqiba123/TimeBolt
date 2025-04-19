from django.urls import path, include
from .views import EndTaskAPI, StartTaskAPI, ExportTasksCSV, home, TasksByDateAPI,SignUpView, welcome

urlpatterns = [
    path('',welcome, name="welcome"),
    path('home/',home, name="home"),
    # path('api/dashboard-stats/', get_dashboard_stats, name='dashboard_stats'),
    path('api/task/start/', StartTaskAPI.as_view(), name="start_task"),
    path('api/task/end/<int:task_id>/', EndTaskAPI.as_view(), name="end_task"),
    path("api/task/export/",ExportTasksCSV.as_view(),name="export_task"),
    path("tasks-by-date/", TasksByDateAPI.as_view(), name="tasks-by-date"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
