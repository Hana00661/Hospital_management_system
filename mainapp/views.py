from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required       #if user is not logged in he will not be able to access this view
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.conf import settings
import requests
import stripe

from mainapp import models as base_models
from doctorapp import models as doctor_models
from patientapp import models as patient_models

def index(request):
    services = base_models.Service.objects.all()        #get all services from the database
    context = {         #pass services to dictionary to be able to access it from the template
        "services": services
    }
    return render(request, "mainapp/index.html", context)

def about_us(request):
    """render about us page"""
    return render(request, "mainapp/pages/about.html")

def contact(request):
    """rendr conntact page"""
    return render(request, "mainapp/pages/contact.html")

def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)    #acquire service from the database, use get because it get just one item

    context = {
        "service": service
    }
    return render(request, "mainapp/service_detail.html", context)

@login_required
def book_appointment(request, service_id, doctor_id):
    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    patient = patient_models.Patient.objects.get(user=request.user)

    if request.method == "POST":        #directly getting the information from the input
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("date_of_birth")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        # Update patient bio data
        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.date_of_birth = date_of_birth
        patient.save()

        # Create appointment object
        appointment =base_models.Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_available_appointment_date,
            issues=issues,
            symptoms=symptoms,
        )

        # Create a billing objects
        billing = base_models.Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = appointment.service.cost * 5 / 100
        billing.total = billing.sub_total + billing.tax
        billing.status = "Unpaid"
        billing.save()

        return redirect("mainapp:checkout", billing.billing_id)

    context = {
        "service": service,
        "doctor": doctor,
        "patient": patient,
    }
    return render(request, "mainapp/book_appointment.html", context)

@login_required
def checkout(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)

    context = {
        "billing": billing,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "paypal_client_id": settings.PAYPAL_CLIENT_ID,
    }
    return render(request, "mainapp/checkout.html", context)

@csrf_exempt
def stripe_payment(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=billing.patient.email,
        payment_method_types=['card'],
        line_items = [
            {
                'price_data': {
                    'currency': 'USD',
                    'product_data': {
                        'name': billing.patient.full_name
                    },
                    'unit_amount': int(billing.total * 100)
                },
                'quantity': 1
            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse("mainapp:stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("mainapp:stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}"

    )
    return JsonResponse({"sessionId": checkout_session.id})     #sessionId is the id of the session that will help us open up a strips hosted pyament page


def stripe_payment_verify(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":
        if billing.status == "Unpaid":
            billing.status = "Paid"
            billing.save()
            billing.appointment.status = "Completed"
            billing.appointment.save()

            doctor_models.Notification.objects.create(
                doctor=billing.appointment.doctor,
                appointment=billing.appointment,
                type="New Appointment"
            )

            patient_models.Notification.objects.create(
                patient=billing.appointment.patient,
                appointment=billing.appointment,
                type="Appointment Scheduled"
            )

            # Prepare data for the email templates
            merge_data = {
                "billing": billing
            }

            # Send appointment email to doctor
            subject = "Hey Doctor, You have a New Appointment"
            text_body = render_to_string("email/new_appointment.txt", merge_data)
            html_body = render_to_string("email/new_appointment.html", merge_data)

            try:
                # Email to Doctor
                msg =  send_mail(
                    subject=subject,
                    message=text_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[billing.appointment.doctor.user.email],
                    html_message=html_body,
                )

                # Email to Patient
                subject = "Appointment Booked Successfully!!"
                text_body = render_to_string("email/appointment_booked.txt", merge_data)
                html_body = render_to_string("email/appointment_booked.html", merge_data)

                msg =  send_mail(
                    subject=subject,
                    message=text_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[billing.appointment.patient.email],
                    html_message=html_body,
                )

            except Exception as e:
                print(f"Email cannot be sent now! Error: {e}")

            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
    else:
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")


def get_paypal_access_token():
    token_url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    data = {'grant_type': 'client_credentials'}
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_ID)
    response = requests.post(token_url, data=data, auth=auth)

    if response.status_code == 200:
        print("Access Token: ", response.json()['access_token'])
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token from PayPal. Status code: {response.status_code}")


def paypal_payment_verify(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)

    transaction_id = request.GET.get("transaction_id")
    print("transaction_id ====", transaction_id)
    paypal_api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{transaction_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_paypal_access_token()}'
    }

    response = requests.get(paypal_api_url, headers=headers)
    print("Response: ", response)
    print("Response Status Code: ", response.status_code)

    if response.status_code == 200:
        paypal_order_data = response.json()
        paypal_payment_status = paypal_order_data['status']

        if paypal_payment_status == "COMPLETED":
            if billing.status == "Unpaid":
                billing.status = "Paid"
                billing.save()
                billing.appointment.status = "Completed"
                billing.appointment.save()

                doctor_models.Notification.objects.create(
                    doctor=billing.appointment.doctor,
                    appointment=billing.appointment,
                    type="New Appointment"
                )

                patient_models.Notification.objects.create(
                    patient=billing.appointment.patient,
                    appointment=billing.appointment,
                    type="Appointment Scheduled"
                )

                merge_data = {
                    "billing": billing
                }

                # Send appointment email to doctor
                subject = "Hey Doctor, You have a New Appointment"
                text_body = render_to_string("email/new_appointment.txt", merge_data)
                html_body = render_to_string("email/new_appointment.html", merge_data)

                try:
                    # Email to Doctor
                    msg =  send_mail(
                        subject=subject,
                        message=text_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[billing.appointment.doctor.user.email],
                        html_message=html_body,
                    )

                    # Email to Patient
                    subject = "Appointment Booked Successfully!!"
                    text_body = render_to_string("email/appointment_booked.txt", merge_data)
                    html_body = render_to_string("email/appointment_booked.html", merge_data)

                    msg =  send_mail(
                        subject=subject,
                        message=text_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[billing.appointment.patient.email],
                        html_message=html_body,
                    )

                except Exception as e:
                    print(f"Email cannot be sent now! Error: {e}")

                return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")

        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")


    return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")


@login_required
def payment_status(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")

    context = {
        "billing": billing,
        "payment_status": payment_status,
    }
    return render(request, "mainapp/payment_status.html", context)
