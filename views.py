from datetime import timedelta, timezone
import datetime
from pyexpat.errors import messages
from tkinter.filedialog import SaveAs
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from library.admin import BookInformationAdmin
from .forms import *
from django.contrib.auth import authenticate, login
from .forms import student_register_form,OTPForm,OTPValidationForm
from .utils import *
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import BookInformation, student_purchase, student_register
from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import BookInformation, student_purchase
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import student_register

from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import student_register

# Assuming validate_otp is the name of the URL pattern for your OTP validation view
from django.urls import reverse

# Create your views here.
def firstpage(request):
    return render(request,"pages/home2.html")


def Registeradmin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            
            # login(request, user)
            return render(request, "pages/dashboard.html")  
        else:
            
            return render(request, "pages/admindashboard.html")  
    else:
       
        return render(request, 'pages/adminlogin.html')




def register_student(request):
    if request.method == 'POST':
        form = student_register_form(request.POST)       
        if form.is_valid():
            # student_id = form.cleaned_data['student_id'] 
            # request.session['bharath']=student_id
            if student_register.objects.filter(**form.cleaned_data).exists():
                return render(request, 'pages/student_already_exists.html')
            else:
                form.save()
                return redirect("student_login_url")
        else:
            return HttpResponse("Invalid form submission.")
    else:
        form = student_register_form()
    return render(request, 'pages/student_register.html', {'form': form})




def student_login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        conform_pass = request.POST.get("conform_pass")
        request.session['email'] = email  

        try:
            member = student_register.objects.get(email=email)
        except student_register.DoesNotExist:
            return HttpResponse("INVALID EMAIL")
        except student_register.MultipleObjectsReturned:
            return HttpResponse("MULTIPLE USERS FOUND, CONTACT ADMIN")
        
        if member.status == 0:
            return HttpResponse("Your registration is pending approval. Please wait for admin confirmation.")
        elif member.status == 1 and member.password == password:
            # Generate OTP
            otp = ''.join(random.choices('0123456789', k=6))
            
            # Save OTP to session
            request.session['otp'] = otp
            request.session['student_id'] = member.student_id
            
            # Send OTP to email
            send_mail(
                'OTP for Login',
                f'Your OTP for login is: {otp}',
                'your_email@example.com',  # Replace with your email address
                [email],
                fail_silently=False,
            )
            return redirect(reverse('otp_validate'))  # Redirect to the OTP validation view
        else:
            return HttpResponse("PASSWORD WRONG OR YOU ARE REJECTED")
    else:   
        return render(request, 'pages/student_login.html')

def dashboard(request):
    return render(request,'pages/dashboard.html')

def send_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = generate_otp()
            request.session['otp'] = otp
            send_mail(
                'Your OTP',
                f'Your OTP is : {otp}',
                'libraryb78@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('otp_validate')
        
    else:
        form = OTPForm()
    return render(request,'pages/otp_form.html',{'form':form})

# from django.shortcuts import render, HttpResponse
# from .forms import OTPValidationForm  
# from .models import BookInformation 

def validate_otp(request):
    if request.method == 'POST':
        
        form = OTPValidationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            stored_otp = request.session.get('otp')

            if stored_otp and entered_otp == stored_otp:
                books = BookInformation.objects.all()  
                return render(request, 'pages/student_dashboard.html', {'books': books})
            else:
                return HttpResponse('Enter correct OTP')
    else:
        form = OTPValidationForm()
    return render(request, 'pages/otp_validation.html', {'form': form})


def admindashboard(request):
    return render(request,"pages/admindashboard.html")


def library_books(request):
    books = BookInformation.objects.all()

    if request.method == 'POST':
        book_name = request.POST['book_name']
        author_name = request.POST['author_name']
        department_name = request.POST['department_name']
        count = request.POST['count']
        BookInformation.objects.create(book_name=book_name, author_name=author_name, department_name=department_name, count=count)
        
        return HttpResponseRedirect(request.path_info)

    return render(request, 'pages/librarybooks.html', {'books': books})

def issued_books(request):
    purchases = student_purchase.objects.all()
    for purchase in purchases:
        time_difference = timezone.now() - purchase.issuedate  
        if time_difference.total_seconds() > (2 * 60): 
           
            intervals = int(time_difference.total_seconds() / (2 * 60))
           
            purchase.penalty = intervals * 2.00  
        else:
            purchase.penalty = None
        purchase.save()  #
    return render(request, 'pages/available_books.html', {'purchases': purchases})


# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from .models import BookInformation
# from flask import session

def purchase_book(request, book_id):
    book = get_object_or_404(BookInformation, pk=book_id)
    
    if request.method == 'POST':
        count = int(request.POST.get('count', 0))
        
        if count > 0:
            if count <= book.count:
                student_id = request.session.get('student_id')
                already_purchased = student_purchase.objects.filter(student_id=student_id, book_name=book.book_name, total=count).exists()
                
                if not already_purchased:
                    book.count -= count
                    book.save()
                    transfer_data(book_id, count, student_id)
                    
                    new_purchase = student_purchase(
                        student_id=student_id,
                        book_name=book.book_name,
                        dept_name=book.department_name,
                        name_of_author=book.author_name,
                        total=count
                    )
                    new_purchase.save()
                    
                    
                    purchases = student_purchase.objects.filter(student_id=student_id)
                    
                    
                    for purchase in purchases:
                        time_difference = timezone.now() - purchase.issuedate
                        if time_difference.total_seconds() > (2 * 60):  
                            purchase.penalty = 2.00  
                        else:
                            purchase.penalty = None
                        purchase.save()  
                    
                    all_books = BookInformation.objects.all()
                    return render(request, 'pages/purchase_confirmation.html', {'book': book, 'purchases': purchases, 'count': count, 'all_books': all_books, 'student': student_id})
                else:
                    return HttpResponse("Error: You have already purchased this book. You cannot purchase it again.")
            else:
                return HttpResponse("Error: Requested count exceeds available count.")
        else:
            return HttpResponse("Error: Invalid count.")
    else:
        return HttpResponse("Error: Method not allowed.")

    

def transfer_data(book_id, count, student_id):
   
    book = get_object_or_404(BookInformation, pk=book_id)

    # No need to create an instance of student_purchase here,
    # as it's already being created in the purchase_book function

    # Update book count and save it
    book.count -= count
    book.save()



# from django.core.mail import send_mail
# from django.shortcuts import redirect, render
# from .models import student_register
# from django.core.mail import send_mail
# from django.shortcuts import redirect, render
# from .models import student_register



def approveorg(request):
    registrations = student_register.objects.all()

    if not registrations:  
        return render(request, 'no_registrations.html')

    for registration in registrations:
        try:
            registration.status = 1
            registration.save()

            subject = 'Registration has been approved'
            message = 'Your registration has been approved. You may now proceed.'
            from_email = 'libraryb78@gmail.com'
            to_email = registration.email
            send_mail(subject, message, from_email, [to_email])
        except Exception as e:
            print(f"Error approving registration: {e}")

    return render(request, 'pages/sucess.html')



# from django.shortcuts import redirect
# from django.core.mail import send_mail
# from .models import student_register

def reject_registration(request):
    if request.method == 'GET':
        registration_id = request.GET.get('registration_id')
        if registration_id:
            try:
                registration = student_register.objects.get(id=registration_id)
                registration.status = 2  
                registration.save()
                subject = 'Registration Rejected'
                message = 'We regret to inform you that your registration has been rejected.'
                from_email = 'libraryb78@gmail.com'
                to_email = registration.email
                send_mail(subject, message, from_email, [to_email])

                return render(request, 'pages/reject.html')
            except student_register.DoesNotExist:
                pass
    return redirect('admin_dashboard') 

def approve(request):
    registrations = student_register.objects.all()  
    return render(request, 'pages/aandrej.html', {'registrations': registrations})
 
# from django.shortcuts import render

# def submit_books_page(request):
#     # Logic for rendering the submit books page goes here
#     return render(request, 'pages/submit_books.html')

from django.http import HttpResponse

def submit_book(request, book_id):
    if request.method == 'POST':
       
        book = get_object_or_404(student_purchase, pk=book_id)
        
       
        bharath = BookInformation.objects.filter(book_name=book.book_name).first()
        
        if bharath:
            # Incrementing count and saving
            bharath.count += 1
            bharath.save()
            
            # Decreasing total in StudentPurchase
            book.total -= 1
            book.save()
            book.delete()
            
            return HttpResponse("Book submitted successfully.")
        else:
            return HttpResponse("Book name not matched")
    else:
        return HttpResponse("No POST request occurred.")
    

def status(request):
    bharath = request.session.get('student_id')  
    purchases = student_purchase.objects.all() 
    for purchase in purchases:
        time_difference = timezone.now() - purchase.issuedate  
        if time_difference.total_seconds() > (2 * 60):  
            intervals = int(time_difference.total_seconds() / (2 * 60))
            purchase.penalty = intervals * 2.00  
        else:
            purchase.penalty = None
        purchase.save()  

    return render(request,'pages/status_check.html',{'purchases':purchases,'student':bharath})

def update_book(request, book_id):
    book = get_object_or_404(BookInformation, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/library_books/')
    else:
        form = BookForm(instance=book)
    return render(request, 'pages/update_book.html', {'form': form})

# def purchase_confirmation(request):
#     student = "Your Student Name"  # You need to provide the student's name
#     purchases = student_purchase.objects.filter(student_id=student)

#     # Calculate penalty for each purchase
#     for purchase in purchases:
#         if datetime.now() > purchase.issuedate + timedelta(minutes=2):  # Change to 2 minutes
#             purchase.penalty = 1  # Apply penalty if the submission is late
#         else:
#             purchase.penalty = None
#     return render(request, 'pages/purchase_confirmation.html', {'student': student, 'purchases': purchases})

def renew_book(request, purchase_id):
    if request.method == 'POST':
        try:
            purchase = student_purchase.objects.get(pk=purchase_id)
        except student_purchase.DoesNotExist:
            return HttpResponse("Purchase with ID {} does not exist".format(purchase_id))
        
        purchase.issuedate += timedelta(minutes=2)
        purchase.submit_date += timedelta(minutes=2)

        purchase.save()
        
        time_difference = timezone.now() - purchase.issuedate
        if time_difference.total_seconds() > (2 * 60):
            purchase.penalty = 2.00
        else:
            purchase.penalty = None
        purchase.save()
        
        return render(request,'pages/success.html')
    else:
        pass
    
def success_page(request):
    return render(request, 'success.html')


def about_us(request):
    return render(request, 'pages/about_us.html')


def dinesh(request):
    return render(request,'pages/dinesh.html')
