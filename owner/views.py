from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
from django.views.generic import View
from owner.form import LoginForm, RegistrationForm,ProductForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home.html")


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return render(request, "login.html")
        else:
            return render(request,"register.html",{"form":form})

class ProductCreateView(View):
    def get(self,request,*args,**kwargs):
        form=ProductForm()
        return render(request,"product-add.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"home.html")
        else:
            return render(request,"product-add.html",{"form":form})


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()

        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        print(request.POST.get('username'))
        print(request.POST.get("password"))
        return render(request, "home.html")
