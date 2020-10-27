from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def index(request):
    """
    View to return the index page
    """
    page_title = "Home Page"
    template = "home/index.html"
    context = {
        'page_title': page_title,
    }
    return render(request, template, context)

def contact(request):
    """
    View to handle the contact page
    instasiate form onto page and handle post request from user
    if form is valid send email
    """
    page_title = "Contact Us"
    admin_email = settings.EMAIL_HOST_USER
    subject = render_to_string(
        'emails/contact_request_subject.txt'
    )
    if request.method == "POST":
        form = Contact(request.POST)

        if form.is_valid():
            reply_email = request.POST.get('email')
            body = render_to_string('emails/contact_request_body.txt')
            subject = render_to_string('emails/contact_request_subject.txt')
            form.save()
            try:
                send_mail(
                    subject,
                    body,
                    reply_email,
                    [admin_email],
                    )
                messages.success(request, 'Your message has been sent successfully')
            except Exception as e:
                messages.error(request, f"Message not sent,Error! {e}")
            return redirect(reverse('contact_success'))
        else:
            messages.error(request,
                           'Sorry something went wrong, please ensure all fields are correctly filled out')
    else:
        form = Contact()

    template = 'home/contact.html'
    context = {
        'page_title': page_title,
        'form':form,
    }
    return render(request, template, context)


def contact_success(request):
    """
    contact_success to return the template,
    page title and context of the view.
    """
    page_title = "Thanks for contacting"
    template = "home/contact_success.html"

    context = {
        'page_title' : page_title
    }

    return render(request, template, context)