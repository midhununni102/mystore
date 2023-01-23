from django.urls import path
from owner import views


urlpatterns=[
    path("register",views.SignUpView.as_view()),
    path("home",views.HomeView.as_view()),
    path("login",views.SignInView.as_view()),
    path("products/add",views.ProductCreateView.as_view())

]