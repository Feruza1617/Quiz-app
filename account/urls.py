from django.urls import path
from .views import RegisterView, LoginAPIView, ChangePasswordCompletedView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('change-password/', ChangePasswordCompletedView.as_view())

]
