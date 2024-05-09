from django.contrib import admin
from .models import *
from .models import BookInformation, student_purchase
from .forms import BookInformationForm,student_purchase_form


class student_register_admin(admin.ModelAdmin):
       list_display = ("student_id","student_name","dept","year","email","password",)
admin.site.register(student_register,student_register_admin)

class BookInformationAdmin(admin.ModelAdmin):
    form = BookInformationForm
    list_display = ['book_name', 'author_name', 'department_name','count',]
    search_fields = ['book_name', 'author_name', 'department_name','count',]

admin.site.register(BookInformation, BookInformationAdmin)


class studentAdmin(admin.ModelAdmin):
    form = student_purchase_form
    list_display = ['student_id','book_name', 'name_of_author', 'dept_name','total','issuedate','submit_date',]
admin.site.register(student_purchase,studentAdmin)

