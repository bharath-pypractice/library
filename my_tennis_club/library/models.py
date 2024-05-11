from datetime import timedelta, timezone  # Correct import statement
from django.db import models
from django.utils.timezone import now  # Import now() method directly

class BookInformation(models.Model):
    book_name = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    department_name = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.book_name
    
class student_purchase(models.Model):
    student_id = models.CharField(max_length=255)
    book_name = models.CharField(max_length=255)
    name_of_author = models.CharField(max_length=255)
    dept_name = models.CharField(max_length=100)
    total = models.IntegerField(default=0)
    issuedate = models.DateTimeField(default=now)  # Use now() directly
    submit_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs): 
        if not self.submit_date:
            self.submit_date = self.issuedate + timedelta(minutes=2)  # Set submit_date after 2 minutes
        super().save(*args, **kwargs)

class student_register(models.Model):
    student_id = models.CharField(max_length=255)
    student_name = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    year = models.DateField()
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=255)
    status = models.IntegerField(default=0)  # 0 for pending, 1 for approved

    def __str__(self):
        return self.email
