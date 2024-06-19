from django.urls import path
from  .import views



urlpatterns = [
    
    path('', views.home, name='home'), 
    path('car/<str:pk>/', views.car,  name='car'),
   # path('customer-form/', views.create_customer, name='customer-form'),  
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_page, name='register'),
    #path('update-customer/<str:pk>/', views.update_customer, name='update-customer'),  
    
    path('', views.available_cars, name='available_cars'),  # Home page 
    path('book/<int:car_id>/', views.book_car, name='book_car'),  
      #path('logout/', views.logout_user, name='logout'),
   
    #path('profile/<str:pk>/', views.user_profile, name='user-profile'),
    #path('update-user', views.update_user, name='update-user')
  
    
    #path('booking_confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    
    
]



# urlpatterns = [
#     path('', views.home, name='home'), 
#     path('car/', views.car_list, name='car_list'),  # Define URL pattern for /car/
#     path('car/<str:pk>/', views.car, name='car'),  # URL pattern for individual car details
# ]

