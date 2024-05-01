from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.user_login, name='login'),
    
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('cab/', views.cab, name='cab'),
    path('cab/account/', views.cab, name='my_acount'),
    path('cab/orders/', views.my_orders, name='my_orders'),
    path('cab/shopping-cart/', views.my_shopping_cart, name='my_shopping_cart'),
    path('cab/wallet/', views.my_wallet, name='my_wallet'),
    path('shop/', views.shop, name='shop'),
    path('shop/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_item/', views.upadateItem, name='update_item'),
    path('cart/', views.cart, name='cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    
    path('successfully/', views.successfully, name='successfully'),
    # Скидання пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
