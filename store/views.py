from operator import mod
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hashlib import md5
from .models import SiteUser, ProductInventory, ProductDetailInfo, Product, ProductCategory
from . import models
from datetime import datetime
# Create your views here.

import pandas as pd


def index(request):

    print("===========================================")
    print("Session Info")
    print(request.session)
    print("Session Key")
    print(request.session.session_key)
    print(request.headers)


    data = models.ProductDetailInfo.objects.all()
    print(data[0:3])
    if request.session.get("userId", -1) != -1:
        return render(request, 'store/index.html', {
            "login": True,
            "active": "home",
            "data": data[3:7]
        })

    return render(request, 'store/index.html', {
        "active": "home",
        "data": data[3:7]
    })


def termAndCondition(request):
    return render(request, 'store/tremAndCondition.html')


def loginForm(request):
    # If already Login Then redirect to Home page
    if request.session.get('userId', -1) != -1:
        return redirect('store:index')

    return render(request, 'store/logIn.html')


def signinForm(request):
    # If already Login Then redirect to Home page
    if request.session.get('userId', -1) != -1:
        return redirect('store:index')

    return render(request, 'store/signin.html')


def logIn(request):

    print("===========================================")
    print("Session Info")
    print(request.session)
    print(request.session.session_key)
    responce = dict()

    if request.method == "POST":

        email = request.POST["userName"]
        print("Email :- ", email)
        pwd = request.POST["password"]

        # If User is not Registered on site
        try:
            user = SiteUser.objects.get(userName=email)
        except:
            return render(request, 'store/logIn.html', {
                "message": "User is Not Registered. Pleases SignIn first",
            })

        encodedData = md5(pwd.encode())
        if user.password == encodedData.hexdigest():
            responce = {
                "companyName": user.userName,
            }
        else:
            return render(request, 'store/logIn.html', {
                "message": "Enter correct User name or Password",
            })
        request.session["userId"] = user.id

        # Check Previous Url
        if request.session.get("previous_url",None) is not None:
            return redirect(f"store:{request.session.get('previous_url')}")

        if request.session.get("product_id", None) is not None:
            return redirect("store:add_item_to_cart")
    else:
        return redirect("store:logInForm")

    return redirect("store:index")


def registration(request):

    if request.method == "POST":
        print("post Method")
        email = request.POST["userName"]
        pwd = request.POST["password"]
        re_pwd = request.POST["Re-password"]
        if email == "" or pwd == "":
            return render(request, "store/signin.html", {"message": "All field are Requried"})
        if pwd != re_pwd:
            return render(request, "store/signin.html", {"message": "Mis matching Password"})

        encodedData = md5(pwd.encode())
        print("Password :- ", encodedData.hexdigest())

        if len(SiteUser.objects.filter(userName=email)) != 0:
            return render(request, "store/signin.html", {
                "message": "User is already exist.Try to Login with credential",
            })
        else:
            user1 = SiteUser(userName=email, password=encodedData.hexdigest())
            user1.save()

        request.session["userId"] = user1.id
        request.session.setdefault("userId",user1.id)
        request.session.set_expiry(3600*4)

        if request.session.get("product_id", None) is not None:
            return redirect("store:add_item_to_cart")

        if request.session.get("previous_url", None) is not None:
            return redirect(f"store:{request.session.get('previous_url')}")

        responce = {
            "userName": email,
            "password": encodedData.hexdigest()
        }
        print("UserName :- ", email)
        print("Password :- ", pwd)
    else:
        return redirect("store:signInForm")

    return redirect("store:index")


def logout(request):
    request.session.set_expiry(-1)
    return redirect("store:logInForm")


def dashboard(request):

    print("===========================================")
    print("Session Info")
    print(request.session)
    print(request.session.session_key)
    print(request.headers)

    if request.session.get("userId", -1) == -1:
        request.session["previous_url"] = "dashboard"
        return redirect("store:logInForm")

    data = []

    cart_product = []
    sop_ses = models.ShoppingSession.objects.filter(
        user_id_id=request.session.get("userId"))
    for i in sop_ses:
        cart_product.append(models.CartItem.objects.get(session_id=i))

    for i in cart_product:
        if i.deletedAt is not None:
            continue

        product_data = {
            "id": i.product_id.id,
            "name": i.product_id.name,
            "img": i.product_id.img_url.url,
            "category": i.product_id.category_id.name.capitalize()
        }
        data.append({
            "product": product_data,
            "cart": i.id,
            "quantity": i.quantity,
            "added_at": i.createdAt
        })

    msg = request.session.get("msg", None)
    if msg is not None:
        request.session.delete(session_key="msg")
        request.session["msg"] = ""
        print("msg")
        print(msg)

    return render(request, 'store/dashboard.html', {
        "login": True,
        "data": data,
        "msg": msg,
    })


# def removeCart(request):
#
#     return redirect("store:d")

def userProfile(request):
    print(request.session.session_key)
    return render(request, 'store/userProfile.html', {
        "login": True,
    })


def aboutUs(request):
    if request.session.get("userId", -1) != -1:
        return render(request, 'store/aboutUs.html', {
            "login": True,
            "active": "aboutUs"
        })

    return render(request, 'store/aboutUs.html', {
        "active": "aboutUs"
    })


# Render Store template with Item Data
def store(request):

    print("===========================================")
    print("Session Info")
    print(request.session)
    print("Session Key")
    print(request.session.session_key)
    print(request.headers)

    products = ProductDetailInfo.objects.all()


    msg = request.session.get("msg", None)
    if msg is not None:
        request.session.delete("msg")
        print("Msg")
        print(msg)
        request.session["msg"] = ""


    if request.session.get("userId", -1) != -1:
        return render(request, 'store/store.html', {
            "login": True,
            "Data": products,
            "active": "store",
            "msg" : msg,
        })

    return render(request, 'store/store.html', {
        "Data": products,
        "active": "store",
    })


# Render Detailed-product page from where customer can add items to cart
def productDetail(request, product_id):

    print("===========================================")
    print("Session Info")
    print(request.session)
    print(request.session.session_key)
    product = ProductDetailInfo.objects.get(productId_id=product_id)
    if request.session.get("userId", -1) != -1:
        return render(request, 'store/productDetail.html', {
            "login": True,
            "detail": product,
            "active": "store",
        })

    print(product)
    return render(request, 'store/productDetail.html', {
        "detail": product,
        "active": "store",
    })


# Add Product to Customer cart
def cartAdd(request):

    print("===========================================")
    print("Session Info")
    print(request.session)
    print(request.session.session_key)
    # check for direct
    if request.POST.get("quantity") is None:
        quantity = request.session.get("quantity")
        product_id = request.session.get("product_id")
    else:
        quantity = request.POST.get("quantity")
        product_id = request.POST.get("product")

    request.session["quantity"] = quantity
    request.session["product_id"] = product_id

    if request.session.get("userId", -1) == -1:
        return redirect("store:logInForm")
    msg = {
        "status": 200,
        "msg": "Success",
    }

    if quantity == "":
        msg["status"] = 301
        msg["msg"] = "Quantity Is not entered"
        return JsonResponse(msg)
    product = models.Product.objects.get(id=product_id)
    total = int(quantity) * int(product.display_price)

    ses = models.ShoppingSession(
        user_id_id=request.session.get("userId"),
        total=total,
    )
    ses.save()

    cart = models.CartItem(
        session_id=ses,
        product_id=product,
        quantity=quantity,
    )
    cart.save()
    request.session.delete("product_id")
    request.session.delete("quantity")

    request.session["msg"] = quantity + " " + product.name + " added to your cart"

    return redirect("store:store")


# change Cart Data
def editCartItem(request, Id):

    print("===========================================")
    print("Session Info")
    print(request.session)
    print(request.session.session_key)
    if request.session.get("userId", -1) == -1:
        return redirect("store:logInForm")

    user_id = request.session.get("userId")

    product = models.Product.objects.get(id=Id)
    session_id = models.ShoppingSession.objects.get(user_id=user_id)
    product_detail = models.ProductDetailInfo.objects.get(productId=product)
    cartDetail = models.CartItem.objects.get(
        session_id=session_id, product_id=product)

    print("Product ")
    print(product)
    print("Session Id")
    print(session_id)
    print("Cart Quantity ")
    print(cartDetail)

    return render(request, "store/editCartItem.html", {
        "product": product_detail,
        "cart": cartDetail.quantity,
    })


# Update Cart Product Item Quantity
def updateCartItem(request):

    print("===========================================")
    print("Session Info")
    print(request.session)
    print(request.session.session_key)
    if request.session.get("userId", -1) == -1:
        return redirect("store:logInForm")

    if request.method == "POST":
        user_id = request.session.get("userId")

        cart_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        cart = models.CartItem.objects.get(id=cart_id)
        if cart.session_id.user_id.id == user_id:
            cart.quantity = quantity
            cart.modifiedAt = datetime.now()
            cart.session_id.total = cart.getTotal()
            cart.save()

        request.session["msg"] = "' " + cart.product_id.name + "'s quantity Updated"

    return redirect("store:dashboard")


# Remove Product From Cart
def removeCartItem(request, Id):

    print("===========================================")
    print("Session Info")
    print(request.session)
    print(request.session.session_key)
    if request.session.get("userId", -1) == -1:
        return redirect("store:logInForm")

    user_id = request.session.get("userId")
    cart = models.CartItem.objects.get(id=Id)
    if cart.session_id.user_id.id == user_id:
        cart.deletedAt = datetime.now()
        cart.save()

        request.session["msg"] = "' " + cart.product_id.name + "' removed From cart"

    return redirect("store:dashboard")


def placeOrder(request):
    print("===========================================")
    print("Session Info")
    print(request.session)
    print(request.session.session_key)

    # check for direct
    if request.POST.get("cart_id") is None:
        if request.POST.get("quantity") is None:
            quantity = request.session.get("quantity")
            product_id = request.session.get("product_id")
        else:
            quantity = request.POST.get("quantity")
            product_id = request.POST.get("product_id")
    else:
        cart = models.CartItem.objects.get(id=request.POST.get("cart_id"))
        cart.deletedAt = datetime.now()
        quantity = request.POST.get("quantity")
        product_id = request.POST.get("product_id")
        cart.quantity = quantity
        cart.product_id.id = product_id
        cart.session_id.modifiedAt = datetime.now()
        cart.save()

    request.session["quantity"] = quantity
    request.session["product_id"] = product_id
    request.session["previous_url"] = "place_order"

    if request.session.get("userId", None) is None:
        return redirect("store:logInForm")

    msg = {
        "status": 200,
        "msg": "Success",
    }

    if quantity == "":
        msg["status"] = 301
        msg["msg"] = "Quantity Is not entered"
        return JsonResponse(msg)

    product = models.Product.objects.get(id=product_id)
    total = int(quantity) * int(product.display_price)

    order_detail = models.OrderDetails(
        user_id_id=request.session.get("userId"),
        total= total
    )
    order_detail.save()
    print("Order Detail : ")
    print(order_detail)

    order_items = models.OrderItems(
        order_id=order_detail,
        product_id=product,
        quantity=quantity
    )
    order_items.save()

    print("Order Items")
    print(order_items)

    detail = models.ProductDetailInfo.objects.get(productId=product)
    request.session.delete("product_id")
    request.session.delete("quantity")

    return render(request, 'store/orderPage.html', {
        "login": True,
        "product": detail,
        "cart": quantity,
        "Order_id" : order_detail,
        "call_bot" : True
    })


def myOrder(request):

    print("===========================================")
    print("Session Info")
    print(request.session)
    print(request.session.session_key)

    if request.session.get("userId", -1) == -1:
        return redirect("store:logInForm")

    orderDetailList = models.OrderDetails.objects.filter(user_id_id=request.session.get("userId"))
    data = []
    for i in orderDetailList:
        tmp = []
        for j in models.OrderItems.objects.filter(order_id=i):
            tmp.append(j)
        data.append({
            "session" : i,
            "product": tmp[0],
        })
    print(data)
    return render(request, "store/myOrders.html", {
        "login": True,
        "data": data
    })


# Temporary Functions for add data into database
def storeDataIn(request):
    csv_data = pd.read_csv("data.csv")
    check = ProductCategory.objects.count()
    if check != 0:
        return JsonResponse({
            "msg": "Data Already presents in Database"
        })

    print("Cetegory Count ",check)
    print(csv_data)
    print("Length ", len(csv_data))
    print(csv_data.head())
    print(csv_data.columns)
    # product_cat = ProductCategory.objects.get(id=1)
    category = ProductCategory(name="Mobile Phone")
    category.save()

    for i in range(0, len(csv_data)):
        # print(csv_data["product_name"][i])
        print(csv_data["product_name"][i])
        tmpName = csv_data["product_name"][i]
        try:
            t = tmpName.split(")")
            tmpName = t[0] + ")"
            tmpDesc = t[1]
        except:
            tmpDesc = ""
            pass
        print("Temp  Name", tmpName)
        print("Temp  Desc", tmpDesc)

        actual_p = csv_data["display_price"][i]
        actual_p = int(actual_p)
        print(actual_p)
        product_item = Product(
            name=tmpName,
            desc=tmpDesc,
            category_id_id=category.id,
            display_price=csv_data["display_price"][i],
            actual_price=actual_p-2000,
            brand=csv_data["brand"][i],
        )
        product_item.save()
        product_inventory = ProductInventory(product_id=product_item,quantity=120)
        product_inventory.save()
        try:
            product_detail = ProductDetailInfo(
                productId=product_item,
                rear_Camara=csv_data["rear_Camara"][i],
                front_camara=csv_data["front_camara"][i],
                ram=csv_data["ram"][i].replace("GB",""),
                inbuilt_storage=csv_data["inbuilt_storage"][i].replace("GB",""),
                expandable_storage=csv_data["expandable_storage"][i].replace("GB",""),
                processor_brand=csv_data["processor_brand"][i],
                operating_system=csv_data["operating_system"][i],
                screen=csv_data["screen"][i],
                battery_power=csv_data["battery_power"][i].replace(" mah",""),
                battery_type=csv_data["battery_type"][i],
            )
            product_detail.save()
        except:
            product_inventory.delete()
            product_item.delete()

    return JsonResponse({
        "msg": "Data inserted in Database Successfully",
        # "data": csv_data
    })


def ProductDataForChatBot(request):

    p_id = request.GET.get("product_id")
    print(p_id)

    temp = Product.objects.get(id=p_id)
    data ={
        "name" : temp.name,
        "display_price": temp.display_price,
        "min_price":temp.actual_price
    }
    return JsonResponse(data)


def confirmOffer(request):

    print("Confirm Order Called")
    if request.method == "POST":
        session_id = request.POST.get("session_id")
        coupon = request.POST.get("coupon")

        orderDetail = models.OrderDetails.objects.get(id=session_id)
        # if orderDetail is not None:
        try:
            if orderDetail.applied_offer.name == coupon:
                discount_per = orderDetail.applied_offer.discount_percent
                tmp = orderDetail.total - (orderDetail.total * float(discount_per) / 100)
                print(tmp)
                orderDetail.discounted_price = tmp
                orderDetail.discount_percentage = discount_per
                orderDetail.save()
        except:
            pass
    return redirect("store:myOrder")


@csrf_exempt
def listenChatBotData(request):

    print("Data Received from Chat bot :- ")
    if request.method == "POST":
        print("Post Method ")
        print(request.POST)
        orderDetail = models.OrderDetails.objects.get(id=request.POST.get("identifier"))
        coupon_code = request.POST.get("coupon_code",None)
        offer = models.Discount(name=coupon_code,discount_percent=float(request.POST.get("discount_percentage")))
        offer.save()
        orderDetail.applied_offer = offer
        print("Orderdetail")
        print(orderDetail)
        orderDetail.save()

    else:
        print("Get Method")
        print(request.GET)
    return JsonResponse({
        "status": 200,
        "msg": "Data Received"
    })