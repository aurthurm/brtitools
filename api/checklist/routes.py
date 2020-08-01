
from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r'', views.AccountProfileViewSet, base_name="accounts")

urlpatterns = [
	path('', views.ChecklistCreateRetrieveAPIView.as_view(), name="checklist-add-retrieve"),
	path('all', views.ChecklistListAPIView.as_view(), name="checklist-list"),
	path('section/add', views.SectionCreateAPIView.as_view(), name="section-add"),
	path('section/all', views.SectionListAPIView.as_view(), name="section-list"),
	path('questions/all', views.QuestionListAPIView.as_view(), name="questions-list"),
	path('questions/add', views.QuestionCreateAPIView.as_view(), name="question-create"),
]

urlpatterns += router.urls

