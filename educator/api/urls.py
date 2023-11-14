from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('djoser.urls.authtoken')),
]
