from django.urls import path
from .views import SignupView, LoginView, GetQuestionView, ResetPasswordView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('get-question/', GetQuestionView.as_view(), name='get-question'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]