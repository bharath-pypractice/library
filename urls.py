from xml.etree.ElementInclude import include
from  django.urls import path
from . import views
urlpatterns = [ 
path('',views.firstpage,name="firstpage"),
path('adminurl/',views.Registeradmin,name="adminurl"),
path('student_register/',views.register_student,name="student_register"),
path("student_login/",views.student_login,name="student_login_url"),
path('dashboard/',views.dashboard,name="dashboard"),
path('otp_form/',views.send_otp,name="otp_form"),
path("otp_validate/",views.validate_otp,name="otp_validate"),
path('admindashboard/',views.admindashboard,name="admindashboard"),
path("library_books/",views.library_books,name="library_books"),
path('update_book/<int:book_id>/', views.update_book, name='update_book'),
path('issued_books/',views.issued_books,name="issued_books"),
path('purchase_book/<int:book_id>/', views.purchase_book, name='purchase_book'),
path('approve/',views.approve,name="approve"),
path('approveorg/',views.approveorg,name="approveorg"),
path('reject-registration/', views.reject_registration, name='reject_registration'),
# path('submit_books/', views.submit_books_page, name='submit_books_page'),
path('submit_book/<int:book_id>/', views.submit_book, name='submit_book'),
path('your_status',views.status,name="your_status"),
# path('purchase_confirmation/', views.purchase_confirmation, name='purchase_confirmation'), 
path('renew_book/<int:purchase_id>/', views.renew_book, name='renew_book'),
path('renew_book/<int:purchase_id>/success/', views.success_page, name='renew_success'),
path('about_us/',views.about_us,name='about_us'),
# path('diensh',views.dinesh,name='dinesh'),
]
