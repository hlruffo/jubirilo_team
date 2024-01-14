from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.api.viewsets import DataModelViewSet

router = DefaultRouter()
router.register(r'data', DataModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    ]
"""
Para consumir esta API, você fará uma requisição POST para o endpoint /data/analyze_data/
"""