from django.db import models
from django.contrib.auth.models import User as users

class Mentor(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="To'liq ism")
    bio = models.TextField(verbose_name="Bio / Tajriba")
    image = models.ImageField(
        upload_to='mentors/%Y/%m/%d/', 
        verbose_name="Rasm",
        blank=True,  # Rasm ixtiyoriy bo'lishi uchun
        null=True    # Rasm bo'lmasa ham bo'ladi
    )
    specialty = models.CharField(
        max_length=225, 
        verbose_name="Mutaxassislik",
        blank=True,  # Bo'sh qoldirish mumkin
        null=True    # NULL bo'lishi mumkin
    )
    instagram = models.URLField(
        max_length=200,
        verbose_name="Instagram profil",
        blank=True,  # Majburiy emas
        null=True    # NULL bo'lishi mumkin
    )
    telegram = models.URLField(
        max_length=200,
        verbose_name="Telegram profil",
        blank=True,  # Majburiy emas
        null=True    # NULL bo'lishi mumkin
    )

    class Meta:
        verbose_name = "Mentor"
        verbose_name_plural = "Mentorlar"
        ordering = ['-id']  # Yangi mentorlarni birinchi ko'rsatish uchun

    def __str__(self):
        return self.full_name

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Kategoriya nomi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Level(models.Model):
    name = models.CharField(max_length=100, verbose_name='Daraja nomi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Daraja'
        verbose_name_plural = 'Darajalar'


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=50)  # masalan: '3 oy'
    image = models.ImageField(upload_to='courses/')
    mentor = models.ForeignKey('Mentor', on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=True)  # Pullik yoki bepul ekanligini belgilash
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Kategoriya')
    level = models.ForeignKey('Level', on_delete=models.SET_NULL, null=True, verbose_name='Daraja')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class CourseEnrollment(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.course.title}"

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Review(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}"

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Xabar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255, verbose_name="Dars nomi")
    description = models.TextField(verbose_name="Tavsif")
    video_url = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_youtube_embed_url(self):
        """Convert YouTube URL to embed URL"""
        if 'youtube.com/watch?v=' in self.video_url:
            video_id = self.video_url.split('watch?v=')[1]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in self.video_url:
            video_id = self.video_url.split('/')[-1]
            return f'https://www.youtube.com/embed/{video_id}'
        return self.video_url

    def clean(self):
        """Clean video URL before saving"""
        if self.video_url:
            # Extract video ID if full URL is provided
            if "youtube.com/watch?v=" in self.video_url:
                self.video_url = self.video_url.split("watch?v=")[1]
            elif "youtu.be/" in self.video_url:
                self.video_url = self.video_url.split("youtu.be/")[1]

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class CompletedLesson(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

class Order(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

class Profile(models.Model):
    user = models.OneToOneField(users, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def delete(self, *args, **kwargs):
        # Delete image file when profile is deleted
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)

class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="Ake.fx haqida", verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, blank=True, verbose_name="Qo'shimcha sarlavha")
    content = models.TextField(verbose_name="Asosiy matn")
    vision = models.TextField(verbose_name="Bizning maqsadimiz", blank=True)
    mission = models.TextField(verbose_name="Bizning vazifamiz", blank=True)
    statistics = models.JSONField(
        default=dict, 
        verbose_name="Statistika", 
        blank=True,
        null=True,  # Qo'shildi
        help_text="Format: {'students': 1200, 'courses': 24, 'mentors': 15, 'satisfaction': 98}"
    )
    team_title = models.CharField(max_length=200, default="Bizning jamoa", verbose_name="Jamoa sarlavhasi")
    team_description = models.TextField(verbose_name="Jamoa haqida", blank=True)
    news_title = models.CharField(max_length=200, default="Yangiliklar", verbose_name="Yangiliklar sarlavhasi")
    news = models.TextField(verbose_name="Yangiliklar (HTML)", blank=True)
    main_image = models.ImageField(upload_to='about/', blank=True, verbose_name="Asosiy rasm")
    video_url = models.URLField(blank=True, verbose_name="Video URL", 
        help_text="YouTube video havolasi")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About sahifa"
        verbose_name_plural = "About sahifa"

    def __str__(self):
        return self.title

    def get_youtube_embed_url(self):
        if 'youtube.com/watch?v=' in self.video_url:
            return self.video_url.replace('watch?v=', 'embed/')
        elif 'youtu.be/' in self.video_url:
            video_id = self.video_url.split('/')[-1]
            return f'https://www.youtube.com/embed/{video_id}'
        return self.video_url

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Yangilik sarlavhasi")
    image = models.ImageField(upload_to='news/', verbose_name="Rasm", blank=True, null=True)
    short_text = models.TextField(verbose_name="Qisqa matn")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
