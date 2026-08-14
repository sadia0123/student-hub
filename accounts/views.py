from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.views import obtain_auth_token

from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


LoginView = obtain_auth_token

from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render


def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/api/dashboard/home/")

        else:

            return render(
                request,
                "login.html",
                {"error": "Invalid username or password"}
            )

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login_page")