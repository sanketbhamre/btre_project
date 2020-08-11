from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Contacts

def contact(request):
    if request.method=='POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if logged user made an enquiry
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contacts.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already inquired')
                return redirect('/listings/'+listing_id)

        contact = Contacts(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone,message=message,
                           user_id=user_id)
        contact.save()

        send_mail(
            'Property Listing Inquiry',
            'There has been inquiry for'+listing+'. Sign in to the admin panel for more info',
            'jab.robert@gmail.com',
            [realtor_email, 'Robert@gmail.com'],
            fail_silently=False


        )
        messages.success(request, 'Your request has been submitted successfully. A realtor wil get back to you soon')
        return redirect('/listings/'+listing_id)