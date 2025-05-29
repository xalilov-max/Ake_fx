from django.contrib import admin
from .models import Mentor, Course, Order, Student, Contact, CourseEnrollment, Lesson, Profile,Category,Level, Review, users

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration')

@admin.register(CourseEnrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    search_fields = ('user__username', 'course__title')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at')
    search_fields = ('title', 'course__title')

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialty', 'instagram', 'telegram')
    search_fields = ('full_name', 'specialty', 'instagram', 'telegram')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'registered_at')
    search_fields = ('full_name', 'email')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_paid', 'created_at')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating', 'date')
    search_fields = ('student__full_name', 'course__title', 'comment')
    list_filter = ('course', 'rating', 'date')

admin.site.register(Category)
admin.site.register(Level)