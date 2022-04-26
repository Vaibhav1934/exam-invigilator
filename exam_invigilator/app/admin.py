from django.contrib import admin
# Register your models here.

from .models import exam,room,faculty,dept,exam_inv
admin.site.register(exam)
admin.site.register(room)
admin.site.register(faculty)
admin.site.register(exam_inv)
admin.site.register(dept)

