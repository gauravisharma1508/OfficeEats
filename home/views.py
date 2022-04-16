from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer, Category, Menu, Order
from django.db.models import Q


class Preview(View):
    def get(self, request, email=None):
        all = Customer.objects.filter(email=email)
        return render(request, "preview.html", {'all': all})

    def post(self, request):
        return render(request, 'signin.html')


class Register(View):
    def get(self, request):
        return render(request, 'regform.html')

    def post(self, request):
        postData = request.POST
        fname = postData.get('fname')
        oname = postData.get('oname')
        emp_id = postData.get('emp_id')
        mob = postData.get('mob')
        email = postData.get('email')
        password = postData.get('password')
        image = request.FILES.get('image')

        value = {'fname': fname, 'oname': oname, 'emp_id': emp_id, 'mob': mob, 'image': image, 'email': email,
                 'password': password}

        customer = Customer(fname=fname, oname=oname, emp_id=emp_id, mob=mob, image=image, email=email,
                            password=password)

        err_msg = self.validateCustomer(customer)

        # saving
        if not err_msg:
            customer.password = make_password(customer.password)
            customer.register()

            all = Customer.objects.filter(email=email)

            return render(request, "preview.html", {'all': all})
            # return  HttpResponse('success')

        else:
            data = {'error': err_msg, 'values': value}
            return render(request, "regform.html", data)

    def validateCustomer(self, customer):
        err_msg = None
        if (not customer.fname):
            err_msg = "Your Name Required!"
        elif (not customer.oname):
            err_msg = "Organizaton Name Required!"
        elif (not customer.emp_id):
            err_msg = "Employee-id Required!"
        elif (not customer.mob):
            err_msg = "Mobile No. required"
        elif not customer.validatePhone():
            err_msg = "Enter valid Mobile no."
        elif len(customer.mob) != 10:
            err_msg = "Mobile No. must have 10 digits"
        elif not customer.validateEmail():
            err_msg = 'Enter valid email'
        elif not customer.password:
            err_msg = "please create a password"
        elif len(customer.password) < 6:
            err_msg = "Password must be 6 char long"
        elif not customer.image:
            err_msg = "please upload id image"
        elif customer.doExists():
            err_msg = 'Email Address Already registered..'
        return err_msg


class Signin(View):
    def get(self, request):
        Signin.return_url = request.GET.get('return_url')
        return render(request, 'signin.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)

        err_msg = None

        if customer:
            flag = check_password(password, customer.password)

            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                request.session['name'] = customer.fname

                if Signin.return_url:
                    return HttpResponseRedirect(Signin.return_url)
                else:
                    Signin.return_url = None
                    return redirect('index')
            else:
                err_msg = 'Email or Password invalid'
        else:
            err_msg = 'Email or Password invalid'
        return render(request, 'signin.html', {'error': err_msg})


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        email = postData.get('email')
        password = postData.get('password')
        val = {'email': email, 'password': password}
        return render(request, 'regform.html', val)


class Dish(View):
    def get(self, request):
        menues = Category.objects.all()
        return render(request, 'menu.html', {'menues': menues})

    def post(self, request):
        return render(request, 'menu.html')


class Index(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        return render(request, 'index.html')

    def post(self, request):
        # menues = Category.objects.all()

        return render(request, 'menu.html')


class Search(View):

    def post(self, request):
        menues = Category.objects.all()
        return render(request, 'search.html', {'menues': menues})

    def get(self, request):
        kw = self.request.GET.get('search')
        products = Category.objects.filter(Q(name__icontains=kw))
        context = {}
        context['products'] = products
        context['kw'] = kw
        return render(request, 'search.html', context)


class Cat(View):

    def post(self, request, pk):
        menues = Menu.get_menu_by_category(category=pk)
        menu = request.POST.get('menu')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(menu)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(menu)
                    else:
                        cart[menu] = quantity - 1
                else:
                    cart[menu] = quantity + 1
            else:
                cart[menu] = 1
        else:
            cart = {}
            cart[menu] = 1

        request.session['cart'] = cart

        return render(request, "category.html", {'menues': menues})

    def get(self, request, pk=None):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        menues = Menu.get_menu_by_category(category=pk)
        return render(request, 'category.html', {'menues': menues})


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        menues = Menu.get_menu_by_id(ids)
        return render(request, 'cart.html', {'menues': menues})


class CheckOut(View):

    def post(self, request):
        payment = request.POST.get('payment')
        phone = request.POST.get('phone')
        takeaway = request.POST.get('takeaway')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        menues = Menu.get_menu_by_id(list(cart.keys()))

        for menu in menues:

            order = Order(customer=Customer(id=customer),
                          menu=menu,
                          price=menu.price,
                          payment=payment,
                          phone=phone,
                          takeaway=takeaway,
                          quantity=cart.get(str(menu.id)))
            if not order.validate2():
                err_msg = "Enter valid Mobile no."
                cart = request.session.get('cart')
                return render(request, 'checkout.html', {'error': err_msg, 'menues': menues})
            elif len(phone) != 10:
                err_msg = "Mobile No. must have 10 digits"
                cart = request.session.get('cart')
                return render(request, 'checkout.html', {'error': err_msg, 'menues': menues})
            else:
                order.save()
                request.session['cart'] = {}
        return redirect('order')

    def get(self, request):
        cart = request.session.get('cart')
        menues = Menu.get_menu_by_id(list(cart.keys()))
        # customer = request.session.get('customer')
        # orders = Order.get_orders_by_customer(customer)
        return render(request, 'checkout.html', {'menues': menues})


class OrderView(View):

    def post(self, request):
        menu = request.POST.get('menu')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(menu)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(menu)
                    else:
                        cart[menu] = quantity - 1
                else:
                    cart[menu] = quantity + 1
            else:
                cart[menu] = 1
        else:
            cart = {}
            cart[menu] = 1

        request.session['cart'] = cart
        return redirect('order')

    def get(self, request):

        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request, 'order.html', {'orders': orders})


def logout(request):
    request.session.clear()
    return redirect('/signin')

