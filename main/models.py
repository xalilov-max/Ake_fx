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
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.full_name} - {self.course.title}'

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
    video_url = models.URLField(verbose_name="Video havolasi", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_youtube_id(self):
        """Extract YouTube video ID from URL"""
        if "youtube.com/watch?v=" in self.video_url:
            return self.video_url.split("watch?v=")[1]
        elif "youtu.be/" in self.video_url:
            return self.video_url.split("youtu.be/")[1]
        return self.video_url
    
    @property
    def get_youtube_embed_url(self):
        """Get proper YouTube embed URL"""
        if not self.video_url:
            return None
            
        video_id = None
        try:
            if "youtube.com/watch?v=" in self.video_url:
                video_id = self.video_url.split("watch?v=")[1].split("&")[0]
            elif "youtu.be/" in self.video_url:
                video_id = self.video_url.split("youtu.be/")[1]
            elif len(self.video_url) == 11:  # Already video ID
                video_id = self.video_url
                
            if video_id:
                return f"https://www.youtube.com/embed/{video_id}?rel=0"
        except:
            return None
        return None

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
    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
