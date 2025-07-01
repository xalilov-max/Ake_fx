from unicodedata import category
from django.shortcuts import render,get_object_or_404, redirect
from .models import CompletedLesson, Course, Lesson, Mentor, Order, Review, Student, Contact, CourseEnrollment,Profile,Category,Level, AboutPage, News, StudentVideo
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from users.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q  # Qidiruv uchun
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
import json

def get_embed_url(video_url):
    if "youtube.com/watch?v=" in video_url:
        return video_url.replace("watch?v=", "embed/")
    elif "youtu.be/" in video_url:
        video_id = video_url.split("/")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    return video_url

def index(request):
    courses = Course.objects.all()[:6]
    mentors = Mentor.objects.all()
    reviews = Review.objects.all()[:3]
    news_list = News.objects.order_by('-created_at')[:3]
    student_videos = StudentVideo.objects.filter(is_active=True).order_by('-created_at')[:6]

    context = {
        'courses': courses,
        'mentors': mentors,
        'reviews': reviews,
        'news_list': news_list,
        'student_videos': student_videos,
    }
    return render(request, 'index.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Email yuborish
            send_mail(
                subject=f"Yangi xabar: {contact.name}",
                message=contact.message,
                from_email=contact.email,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            messages.success(request, "Xabaringiz yuborildi va saqlandi!")
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def review_list(request):
    reviews = Review.objects.all().select_related('student', 'course')
    return render(request, 'review_list.html', {'reviews': reviews})


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

@login_required
def enroll_course(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        if not course_id:
            messages.error(request, "Kurs tanlanmadi!")
            return redirect('course_list')
            
        course = get_object_or_404(Course, id=course_id)
        
        if CourseEnrollment.objects.filter(user=request.user, course=course).exists():
            messages.warning(request, f"Siz allaqachon {course.title} kursiga yozilgansiz!")
            return redirect('dashboard')
        
        # Yangi yozilish yaratish
        CourseEnrollment.objects.create(user=request.user, course=course)
        
        # Elektron pochta xabari yuborish
        send_mail(
            subject=f"Yangi kursga yozilish: {request.user.username}",
            message=f"{request.user.get_full_name()} ({request.user.username}) {course.title} kursiga yozildi.\n\nKurs narxi: {course.price}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_EMAIL, request.user.email],
            fail_silently=True
        )
        
        messages.success(request, f"{course.title} kursiga muvaffaqiyatli yozildingiz!")
        return redirect('dashboard')
    
    # Agar GET so'rov bo'lsa, kurslar ro'yxatiga yo'naltiramiz
    messages.info(request, "Kursga yozilish uchun kursni tanlang")
    return redirect('course_list')

def course_detail(request, course_id):  # Changed from pk to course_id
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.all()
    completed_lessons = []
    
    if request.user.is_authenticated:
        completed_lessons = CompletedLesson.objects.filter(
            user=request.user,
            lesson__course=course
        ).values_list('lesson_id', flat=True)

    context = {
        'course': course,
        'lessons': lessons,
        'completed_lessons': completed_lessons,
    }
    return render(request, 'course_detail.html', context)

@csrf_exempt
@login_required
def complete_lesson(request):
    if request.method == "POST":
        lesson_id = request.POST.get("lesson_id")
        lesson = get_object_or_404(Lesson, id=lesson_id)
        already_completed = CompletedLesson.objects.filter(user=request.user, lesson=lesson).exists()
        
        if not already_completed:
            CompletedLesson.objects.create(user=request.user, lesson=lesson)
            return JsonResponse({"message": "Dars o‘tildi!"}, status=200)
        return JsonResponse({"message": "Siz allaqachon bu darsni o‘tib bo‘lgansiz!"}, status=400)
    return JsonResponse({"error": "Noto‘g‘ri so‘rov"}, status=400)

def mentor_list(request):
    mentors = Mentor.objects.all()
    return render(request, 'mentor_list.html', {'mentors': mentors})

def mentor_detail(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    courses = Course.objects.filter(mentor=mentor)
    return render(request, 'mentor_detail.html', {'mentor': mentor, 'courses': courses})

@login_required
def course_buy(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Kurs allaqachon sotib olinganligini tekshirish
    if Order.objects.filter(user=request.user, course=course, is_paid=True).exists():
        messages.warning(request, f"Siz allaqachon {course.title} kursini sotib olgansiz!")
        return redirect('course_detail', course_id=course.id)

    # Yangi buyurtma yaratish
    order = Order.objects.create(user=request.user, course=course)

    # Click uz uchun to'lov havolasini yaratish
    click_url = f"https://my.click.uz/services/pay?amount={course.price}&merchant_id=YOUR_MERCHANT_ID&transaction_param={order.id}&service_id=YOUR_SERVICE_ID&return_url=http://localhost:8000/payment/callback"

    messages.info(request, f"{course.title} kursini sotib olish uchun to'lov sahifasiga yo'naltirildingiz.")
    return redirect(click_url)

@csrf_exempt
def payment_callback(request):
    order_id = request.GET.get('transaction_param')
    try:
        order = Order.objects.get(id=order_id)
        order.is_paid = True
        order.save()

        # Foydalanuvchiga xabar yuborish
        messages.success(request, f"{order.course.title} kursini muvaffaqiyatli sotib oldingiz!")
        return redirect('course_detail', course_id=order.course.id)
    except Order.DoesNotExist:
        messages.error(request, "Buyurtma topilmadi.")
        return redirect('courses_list')

@login_required
def lesson_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all().order_by('order')
    completed_lessons = CompletedLesson.objects.filter(
        user=request.user,
        lesson__course=course
    )
    
    context = {
        'course': course,
        'lessons': lessons,
        'completed_lessons': completed_lessons,
    }
    
    return render(request, 'lesson_list.html', context)

def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Kursni sotib olganlik tekshiruvi
    has_access = Order.objects.filter(
        user=request.user, 
        course=course,
        is_paid=True
    ).exists()
    
    if not has_access and course.is_paid:
        messages.error(request, "Bu darsni ko'rish uchun kursni sotib olishingiz kerak")
        return redirect('course_detail', course_id=course.id)
    
    # Barcha darslar ro'yxati
    lessons = course.lessons.all().order_by('id')
    
    # Tugatilgan darslar
    completed_lessons = CompletedLesson.objects.filter(
        user=request.user,
        lesson__course=course
    ).values_list('lesson_id', flat=True)
    
    context = {
        'course': course,
        'current_lesson': lesson,
        'lessons': lessons,
        'completed_lessons': completed_lessons,
        'video_url': lesson.get_youtube_embed_url()
    }
    
    return render(request, 'lesson_detail.html', context)


@login_required
def profile(request):
    if not request.user.is_superuser:
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        # Yozilgan kurslar va progress
        enrollments = CourseEnrollment.objects.filter(
            user=request.user
        ).select_related('course')
        
        # Progress hisoblab chiqish
        for enrollment in enrollments:
            enrollment.calculate_progress()
        
        context = {
            'profile': profile,
            'enrollments': enrollments,
            'enrolled_courses_count': enrollments.count(),
        }
        
        return render(request, 'profile.html', context)
    else:
        messages.warning(request, "Admin foydalanuchilar uchun profil mavjud emas.")
        return redirect('admin:index')  # Admin panelga qaytarish

@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get_or_create(user=user)[0]

        # Update user info
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        # Update profile info
        profile.bio = request.POST.get('bio', '')
        profile.save()

        messages.success(request, 'Profil muvaffaqiyatli yangilandi')
        return redirect('profile')

    return redirect('profile')

@login_required
def profile_image_update(request):
    if request.method == 'POST' and request.FILES.get('image'):
        profile = Profile.objects.get_or_create(user=request.user)[0]
        
        # Delete old image if exists
        if profile.image:
            profile.image.delete()
        
        profile.image = request.FILES['image']
        profile.save()
        
        messages.success(request, 'Profil rasmi muvaffaqiyatli yangilandi')
        return redirect('profile')
    
    messages.error(request, 'Rasm yuklashda xatolik yuz berdi')
    return redirect('profile')

def search(request):
    query = request.GET.get('q', '')  # Qidiruv so'zi
    courses = Course.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else Course.objects.none()  # Qidiruv natijalari

    return render(request, 'search_results.html', {'query': query, 'courses': courses})

@login_required
def admin_dashboard(request):
    # Umumiy foydalanuvchilar soni
    total_users = User.objects.count()

    # Kurslar soni
    total_courses = Course.objects.count()

    # Sotilgan kurslar soni
    total_orders = Order.objects.filter(is_paid=True).count()

    # Mentorlardan top 5 tasi (kurslar soni bo'yicha)
    top_mentors = Mentor.objects.annotate(course_count=Count('course')).order_by('-course_count')[:5]

    # So'nggi 7 kun uchun sanalar
    last_7_days = [now().date() - timedelta(days=i) for i in range(6, -1, -1)]

    # Foydalanuvchi o‘sishi
    user_growth = [
        User.objects.filter(date_joined__date=day).count() for day in last_7_days
    ]

    # Kurs qo‘shilishi
    course_growth = [
        Course.objects.filter(created_at__date=day).count() for day in last_7_days
    ]

    context = {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_orders': total_orders,
        'top_mentors': top_mentors,
        'user_growth': json.dumps(user_growth),
        'course_growth': json.dumps(course_growth),
        'last_7_days': json.dumps([day.strftime('%Y-%m-%d') for day in last_7_days]),
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def add_review(request):
    if request.method == "POST":
        course_id = request.POST.get('course')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Foydalanuvchining student obyektini olish
        try:
            student = Student.objects.get(email=request.user.email)
        except Student.DoesNotExist:
            messages.error(request, "Siz student sifatida ro'yxatdan o'tmagansiz.")
            return redirect('index')  # <-- o'zgardi

        course = get_object_or_404(Course, id=course_id)

        # Student kursga yozilganmi?
        if not CourseEnrollment.objects.filter(user=request.user, course=course).exists():
            messages.error(request, "Siz bu kursga yozilmagansiz")
            return redirect('index')  # <-- o'zgardi

        # Bir kursga bir marta sharh
        if Review.objects.filter(student=student, course=course).exists():
            messages.error(request, "Siz bu kursga allaqachon sharh qoldirgansiz")
            return redirect('index')  # <-- o'zgardi

        Review.objects.create(
            student=student,
            course=course,
            rating=int(rating),
            comment=comment
        )
        messages.success(request, "Sharhingiz muvaffaqiyatli qo'shildi")
        return redirect('index')  # <-- o'zgardi
    return redirect('index')  # <-- o'zgardi

@login_required
def delete_review(request, review_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(id=review_id, user=request.user)
            review.delete()
            messages.success(request, "Sharh muvaffaqiyatli o'chirildi")
            return JsonResponse({'success': True})
        except Review.DoesNotExist:
            messages.error(request, "Sharh topilmadi yoki sizga tegishli emas")
            return JsonResponse({'success': False, 'error': 'Sharh topilmadi'}, status=404)
    
    return JsonResponse({'success': False, 'error': 'Noto\'g\'ri so\'rov'}, status=400)

def about(request):
    about = AboutPage.objects.first()
    if not about:
        about = AboutPage(
            title="Ake.fx haqida",
            content="Ake.fx — zamonaviy trading va ta'lim platformasi.",
            statistics={
                'students': 0,
                'courses': 0,
                'mentors': 0,
                'satisfaction': 0
            }
        )
        about.save()

    # So'nggi 4 ta yangilikni olish
    news_list = News.objects.order_by('-created_at')[:4]
    
    context = {
        'about': about,
        'has_stats': bool(about.statistics),
        'has_team': bool(about.team_title and about.team_description),
        'has_video': bool(about.video_url),
        'news_list': news_list,
    }
    
    return render(request, 'about.html', context)

def news_list(request):
    """Barcha yangiliklar ro'yxati"""
    news_list = News.objects.order_by('-created_at')
    
    context = {
        'news_list': news_list,
        'latest_news': news_list.first() if news_list.exists() else None,
    }
    return render(request, 'news/news_list.html', context)

def news_detail(request, news_id):
    """Yangilik tafsilotlari sahifasi"""
    news = get_object_or_404(News, id=news_id)
    # O'xshash yangiliklar (optional)
    related_news = News.objects.exclude(id=news_id).order_by('-created_at')[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'news/news_detail.html', context)