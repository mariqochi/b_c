from .models import Car, Type, User   #,Customer #, Booking
from django.shortcuts import render, redirect
#from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


from django.contrib.auth.decorators import login_required
  # Change: Added import for User model
from .forms import UserForm, MyUserCreationForm   # CustomerForm  # Change: Added import for UserForm and CustomerForm
from django.core.exceptions import ValidationError
from .models import Car
from .forms import BookingForm



from .forms import MyUserCreationForm, UserForm




def home(request):
    query = request.GET.get('q', "")
    
    cars = Car.objects.filter(
        Q(car_type__name__icontains=query) | 
        Q(model__icontains=query) | 
        Q(make__icontains=query)
    )
    
    types = Type.objects.all()
    
    context = {'cars': cars, 'types': types}
    return render(request, 'base/home.html', context)


def register_page(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        user_form = UserForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # Assuming User model has a OneToOneField to a profile model where first_name, last_name, phone, email are stored
            profile = user.profile  # Replace with the actual related name
            profile.first_name = user_form.cleaned_data['first_name']
            profile.last_name = user_form.cleaned_data['last_name']
            profile.phone = user_form.cleaned_data['phone']
            profile.email = user_form.cleaned_data['email']
            profile.save()
            login(request, user)
            return redirect('home')  # Redirect to home or another page upon successful registration
    else:
        form = MyUserCreationForm()
        user_form = UserForm()

    return render(request, 'base/user_registration_old.html', {'form': form, 'user_form': user_form})


# def register_page(request):
#     form = MyUserCreationForm()
#     if request.method == "POST":
#         form = MyUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             login(request, user)
#             return redirect('home')
#     return render(request, 'base/user_registration_old.html', {'form': form})

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username doesn't exist")
            return render(request, 'base/login.html', {})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect")
    
    return render(request, 'base/login.html')



@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, "base/update-user.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')



def car(request, pk):
    car = Car.objects.get(id=int(pk))
    context = {'car': car}
    return render(request, 'base/car.html', context)






@login_required
def create_booking(request, car_id):
    car = Car.objects.get(pk=car_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            try:
                booking.clean()  # Validate availability
            except ValidationError as e:
                form.add_error(None, e)
                return render(request, 'base/book_car.html', {'form': form})

            booking.save()
            return redirect('booking_success')  # Redirect to a success page or view
    else:
        form = BookingForm(initial={'car': car})
    
    return render(request, 'base/book_car.html', {'form': form})





def available_cars(request):
    # Retrieve available cars logic goes here
    cars = Car.objects.filter(is_available=True)  # Example logic to filter available cars

    context = {
        'cars': cars
    }
    return render(request, 'base/available_cars.html', context)



def book_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Assuming the user is logged in
            booking.car = car
            try:
                booking.clean()
                booking.save()
                messages.success(request, 'You have booked the car successfully!')
                return redirect('')  # Redirect to the home page
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = BookingForm()

    return render(request, 'base/book_car.html', {'car': car, 'form': form})



# def create_customer(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         customer_form = CustomerForm(request.POST, request.FILES)
#         if user_form.is_valid() and customer_form.is_valid():
#             # Save the User form first
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password'])
#             user.save()

#             # Save the Customer form, linking it to the User
#             customer = customer_form.save(commit=False)
#             customer.user = user
#             customer.save()

#             return redirect('home')
#     else:
#         user_form = UserForm()
#         customer_form = CustomerForm()
    
#     context = {'user_form': user_form, 'customer_form': customer_form}
#     return render(request, 'base/customer_form.html', context)








# def create_customer(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         customer_form = CustomerForm(request.POST, request.FILES)
#         if user_form.is_valid() and customer_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password1'])  # Corrected password field name
#             user.save()

#             customer = customer_form.save(commit=False)
#             customer.user = user  # Assign user to customer
#             customer.save()

#             # Add success message
#             messages.success(request, "You have registered successfully!")
#             return redirect('home')  # Redirect to home or appropriate URL after successful registration
#     else:
#         user_form = UserForm()  # Initialize user_form in the GET request
#         customer_form = CustomerForm()

#     context = {'user_form': user_form, 'customer_form': customer_form}
#     return render(request, 'base/customer_form.html', context)




# def create_customer(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         customer_form = CustomerForm(request.POST, request.FILES)
#         if user_form.is_valid() and customer_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password1'])  # Change: Corrected password field name
#             user.save()

#             customer = customer_form.save(commit=False)
#             customer.user = user  # Change: Assign user to customer
#             customer.save()

#             # Add success message
#             messages.success(request, "You have registered successfully!")
#             return redirect('home')
#     else:
#         user_form = UserForm()  # Change: Initialize user_form in the GET request
#         customer_form = CustomerForm()

#     context = {'user_form': user_form, 'customer_form': customer_form}  # Change: Added user_form to context
#     return render(request, 'base/customer_form.html', context)



# def create_customer(request):
#     form=CustomerForm()
#     if request.method=='POST':
#         #print(request.POST)
#         form=CustomerForm(request.POST)
#         if form.is_valid():  #davamatot shezgidvebi aucilebel velebze
#             form.save()
#             return redirect('home')
            
#     context= {'form': form}
#     return render(request, 'base/customer_form.html', context)

# def update_customer(request, pk):
#     customer= Customer.objects.get(id=pk)
#     form= CustomerForm(instance=customer)
#     context = {'form': form}
#     return render(request, 'base/customer_form.html', context)

# @login_required
# def update_customer(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     #customer = get_object_or_404(Customer, user=user)
    
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=user)
#         customer_form = CustomerForm(request.POST, request.FILES, instance=customer)
#         if user_form.is_valid() and customer_form.is_valid():
#             user = user_form.save(commit=False)
#             if 'password' in user_form.cleaned_data and user_form.cleaned_data['password']:
#                 user.set_password(user_form.cleaned_data['password'])
#             user.save()

#             customer = customer_form.save(commit=False)
#             customer.user = user
#             customer.save()

#             return redirect('home')
#         else:
#             print("User form errors:", user_form.errors)
#             print("Customer form errors:", customer_form.errors)
#     else:
#         user_form = UserForm(instance=user)
#         customer_form = CustomerForm(instance=customer)
    
#     context = {'user_form': user_form, 'customer_form': customer_form}
#     return render(request, 'base/customer_form.html', context)



# def login_page(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
        
#         try:
#             user = User.objects.get(username=username)  # Fetch user by username
#         except User.DoesNotExist:  # Specify the exact exception
#             messages.error(request, "Username doesn't exist")
#             return render(request, 'base/customer_form.html', {})
        
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, "Username or Password is incorrect")
    
#     context = {}
#     return render(request, 'base/customer_form.html', context)

# @login_required
# def available_cars(request):
#     cars = Car.objects.filter(available=True)
#     return render(request, 'base/available_cars.html', {'cars': cars})

# @login_required
# def book_car(request, car_id):
#     car = get_object_or_404(Car, id=car_id)
#     customer = get_object_or_404(Customer, email=request.user.email)  # Assuming customer's email matches the user's email

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.customer = customer
#             booking.car = car
#             booking.save()
#             return redirect('booking_confirmation', booking_id=booking.id)
#     else:
#         form = BookingForm()
#     return render(request, 'base/book_car.html', {'form': form, 'car': car})

# @login_required
# def booking_confirmation(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     return render(request, 'base/booking_confirmation.html', {'booking': booking})





# def book_car(request, car_id):
#     car = get_object_or_404(Car, pk=car_id)
#     # Additional logic for booking the car can go here
#     return render(request, 'base/book_car.html', {'car': car})


# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from .models import Car

# def book_car(request, car_id):
#     car = get_object_or_404(Car, pk=car_id)
#     if request.method == 'POST':
#         # Process booking logic here
#         return HttpResponse("Booking successful!")  # Replace with appropriate response
    
#     return render(request, 'base/book_car.html', {'car': car})









# def home(request):
#     context= {'cars': cars}
#     return render(request, 'base/home.html', context)

# def car(request):
#     return render(request, 'base/car.html')


# def home(request):
#     q=request.GET.get('q') if request.GET.get('q') != None else ""
    
#     #cars = Car.objects.all()  # Fetch all cars or filter them as per your requirement
#     # Filter cars based on the name field of the related Type model
#     cars = Car.objects.filter(Q(car_type__icontains=q) | Q(model__icontains=q) | Q(make__icontains=q)|Q(num_seats__icontains=q))  
                            
                           
#                              #if q else Car.objects.all()
#     #cars = Car.objects.filter(car_type__name=q) if q else Car.objects.all()
#     #cars=Type.objects.filter(type__name=q)
#     types=Type.objects.all()
#     context = {'cars': cars, 'types': types}
#     return render(request, 'base/home.html', context)


