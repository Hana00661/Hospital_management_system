from django.urls import path
from mainapp import views

app_name = "mainapp"        # This sets the namespace

urlpatterns = [
    path("", views.index, name="index"),
    path("service/<service_id>/", views.service_detail, name="service_detail"),
    path("redirector", views.doctor_redirect, name="doctor_redirect"),
    path("book-appointment/<service_id>/<doctor_id>/", views.book_appointment, name="book_appointment"),
    path("checkout/<billing_id>/", views.checkout, name="checkout"),
    path("payment_status/<billing_id>/", views.payment_status, name="payment_status"),

    path("stripe_payment/<billing_id>/", views.stripe_payment, name="stripe_payment"),
    path("stripe_payment_verify/<billing_id>/", views.stripe_payment_verify, name="stripe_payment_verify"),
    path("paypal_payment_verify/<billing_id>/", views.paypal_payment_verify, name="paypal_payment_verify"),
    path("about_us", views.about_us, name="about"),
    path("contact", views.contact, name="contact"),
]