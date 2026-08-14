from django.urls import path


from .views import LoginView, RegisterView, user_logout, login_page


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView, name='login'),
    path("logout/", user_logout, name="logout"),
    path("login-page/", login_page, name="login_page"),
]