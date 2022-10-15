from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username','user_type']

admin.site.register(CustomUser,UserModel)
admin.site.register(Course)
admin.site.register(Session_year)
admin.site.register(Year_Part)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Staff_Notification)
admin.site.register(Staff_Feedback)
admin.site.register(Student_Notification)
admin.site.register(Student_Feedback)
admin.site.register(StudentResult)
admin.site.register(StudentReport)
admin.site.register(Internal_mark)
admin.site.register(Regular_board_exam)
admin.site.register(Back_board_exam)