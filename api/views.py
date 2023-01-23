from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Products,Carts,Reviews
from api.serializers import ProductSerializers, ProductModelSerializer,UserSerializer,CartSerializer,ReviewSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

class ProductView(APIView):

    def get(self, request, *args, **kwargs):
        qs = Products.objects.all()
        serializers = ProductSerializers(qs, many=True)
        return Response(data=serializers.data)

    def post(self, request, *args, **kwargs, ):
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            Products.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class ProductDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        qs = Products.objects.get(id=id)
        serializer = ProductSerializers(qs, many=False)

        return Response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")
        Products.objects.filter(id=id).update(**request.data)
        qs = Products.objects.get(id=id)
        serializer = ProductSerializers(qs, many=False)

        return Response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        Products.objects.filter(id=id).delete()
        return Response(data="object deleted")


class ProductViewsetView(viewsets.ModelViewSet):
    serializer_class=ProductModelSerializer
    queryset=Products.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # def list(self, request, *args, **kwargs):
    #
    #     qs = Products.objects.all()
    #     serializers = ProductModelSerializer(qs, many=True)
    #     return Response(data=serializers.data)
    #
    # def create(self, request, *args, **kwargs):
    #     serializers = ProductModelSerializer(data=request.data)
    #     if serializers.is_valid():
    #         serializers.save()
    #         return Response(data=serializers.data)
    #     else:
    #         return Response(data=serializers.errors)
    # def retrieve(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     qs=Products.objects.get(id=id)
    #     serializers=ProductModelSerializer(qs,many=False)
    #     return Response(data=serializers.data)
    # def destroy(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     Products.objects.filter(id=id).delete()
    #     return Response(data="deleted")
    #
    # def update(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     obj=Products.objects.get(id=id)
    #     serializer=ProductModelSerializer(data=request.data,instance=obj)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
    @action(methods=["GET"],detail=False)
    def categories(self,*args,**kwargs):
        res=Products.objects.values_list("category",flat=True).distinct()
        return Response(data=res)

    @action(methods=["POST"],detail=True)
    def addto_cart(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        item=Products.objects.get(id=id)
        user=request.user
        user.carts_set.create(products=item)
        return Response(data="item added to cart")

    @action(methods=["POST"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Products.objects.get(id=id)
        user=request.user
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(products=object,User=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["GET"],detail=True)
    def reviews(self,request,*args,**kwargs):
        product=self.get_object()
        qs=product.reviews_set.all()
        serializer=ReviewSerializer(qs,many=True)
        return Response(data=serializer.data)



class CartsView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)
    # def list(self, request, *args, **kwargs):
    #     qs=request.user.carts_set.all()
    #     serializer=CartSerializer(qs,many=True)
    #     return Response(data=serializer.data)


class UsersView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


    # def create(self,request,*args,**kwargs):
    #     serializer=UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

class ReviewDeleteView(APIView):
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Reviews.objects.filter(id=id).delete()
        return Response(data="review deleted")