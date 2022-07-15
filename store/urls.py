from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "store"
urlpatterns = [
    path('', views.index, name="index"),
    path('termCondition', views.termAndCondition, name="termAndCondition"),
    path('logIn', views.loginForm, name="logInForm"),
    path('signIn', views.signinForm, name="signInForm"),
    path('logOut', views.logout, name="logOut"),
    path('signInValidation', views.registration, name="signIn"),
    path('logInValidation', views.logIn, name="logIn"),
    path('Dashboard', views.dashboard, name="dashboard"),
    path('userProfile', views.userProfile, name="userProfile"),
    path('cart', views.cartAdd, name="add_item_to_cart"),
    path('placeOrder', views.placeOrder, name="placeOrder"),
    path('confirmOffer', views.confirmOffer, name="confirmOffer"),
    path('order', views.myOrder, name="myOrder"),
    path('cartEdit/<int:Id>', views.editCartItem, name="edit_cart_item"),
    path('updateCartItem/', views.updateCartItem, name="update_cart_item"),
    path('removeCartItem/<int:Id>', views.removeCartItem, name="remove_cart_item"),

    path('placeOrder', views.placeOrder, name="place_order"),
    path('aboutUs', views.aboutUs, name="aboutUs"),
    path('store', views.store, name="store"),
    path('test', views.storeDataIn, name="test"),
    path('productDetail/<int:product_id>', views.productDetail, name="productDetail"),

    path('ProductInfo', views.ProductDataForChatBot, name="productData"),
    path('chatbotData', views.listenChatBotData, name="chatBotData"),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)