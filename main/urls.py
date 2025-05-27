from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('reviews/', views.review_list, name='review-list'),
    path('courses/', views.course_list, name='courses_list'),
    path('enroll/', views.enroll_course, name='enroll_course'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('complete_lesson/', views.complete_lesson, name='complete_lesson'),
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentor/<int:mentor_id>/', views.mentor_detail, name='mentor_detail'),
    path('course/<int:course_id>/lessons/', views.lesson_list, name='lesson_list'),
    path('course/<int:course_id>/buy/', views.course_buy, name='course_buy'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/image/update/', views.profile_image_update, name='profile_image_update'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='main/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='main/password_change_done.html'), name='password_change_done'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('search/', views.search, name='search'),  # Qidiruv uchun URL
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
