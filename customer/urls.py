
from django.urls import path
from customer import views
urlpatterns=[
    path("register",views.SignUpView.as_view(),name="register"),
    path("",views.SigninView.as_view(),name="signin"),
    path("customers/home",views.HomeView.as_view(),name="user-home"),
    path("products/details/<int:id>",views.ProductDetailView.as_view(),name="product-detail"),
    path("products/carts/<int:id>/add",views.addto_cart,name="add-cart"),
    path("carts/all",views.CartListView.as_view(),name="cart-list"),
    path("orders/add/<int:cid>/<int:pid>",views.OrderView.as_view(),name="place-order"),
    path("orders/all",views.MyOrdersView.as_view(),name="my-orders"),
    path("orders/<int:id>/remove",views.cancelorder_view,name="order-cancel"),
    path("customers/accounts/signout",views.logout_view,name="signout")
]