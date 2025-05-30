from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Mentor, Course, Order, Student, Contact, 
    CourseEnrollment, Lesson, Profile, Category, 
    Level, Review, AboutPage, News
)

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'subtitle', 'content', 'main_image')
        }),
        ('Maqsad va Vazifalar', {
            'fields': ('vision', 'mission'),
            'classes': ('collapse',)
        }),
        ('Statistika', {
            'fields': ('statistics',),
            'description': 'JSON formatida statistika: {"students": 1200, "courses": 24, ...}',
            'classes': ('collapse',)
        }),
        ('Jamoa', {
            'fields': ('team_title', 'team_description'),
            'classes': ('collapse',)
        }),
        ('Yangiliklar', {
            'fields': ('news_title', 'news'),
            'classes': ('collapse',)
        }),
        ('Video', {
            'fields': ('video_url',),
            'classes': ('collapse',)
        })
    )
    
    list_display = (
        'title', 
        'show_main_image', 
        'show_vision',
        'show_mission', 
        'updated_at'
    )
    
    readonly_fields = ('updated_at',)
    search_fields = ('title', 'content', 'news')
    save_on_top = True

    def show_main_image(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;" />',
                obj.main_image.url
            )
        return "Rasm yo'q"
    show_main_image.short_description = 'Asosiy rasm'

    def show_vision(self, obj):
        return obj.vision[:50] + '...' if obj.vision else '-'
    show_vision.short_description = 'Maqsad'

    def show_mission(self, obj):
        return obj.mission[:50] + '...' if obj.mission else '-'
    show_mission.short_description = 'Vazifa'

    def save_model(self, request, obj, form, change):
        if not obj.statistics:
            obj.statistics = {
                'students': 0,
                'courses': 0,
                'mentors': 0,
                'satisfaction': 0
            }
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }
        js = ('js/admin_about.js',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'show_message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

    def show_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    show_message.short_description = 'Xabar'


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'description', 'video_url', 'duration', 'order', 'is_free')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('title', 'price', 'mentor', 'is_paid', 'lesson_count')
    search_fields = ('title', 'description')
    list_filter = ('is_paid', 'mentor')

    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Darslar soni'


@admin.register(CourseEnrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    list_filter = ('enrolled_at', 'course')
    search_fields = ('user__username', 'course__title')
    date_hierarchy = 'enrolled_at'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'show_video_url', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description')
    autocomplete_fields = ['course']

    def show_video_url(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Video havolasi</a>',
            obj.video_url
        ) if obj.video_url else '-'
    show_video_url.short_description = 'Video'


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialty', 'show_image', 'show_social_links')
    list_filter = ('specialty',)
    search_fields = ('full_name', 'bio', 'specialty')
    
    def show_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.image.url
            )
        return "Rasm yo'q"
    show_image.short_description = 'Rasm'

    def show_social_links(self, obj):
        links = []
        if obj.instagram:
            links.append(f'<a href="{obj.instagram}" target="_blank">Instagram</a>')
        if obj.telegram:
            links.append(f'<a href="{obj.telegram}" target="_blank">Telegram</a>')
        return format_html(' | '.join(links)) if links else '-'
    show_social_links.short_description = 'Ijtimoiy tarmoqlar'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating', 'show_comment', 'date')
    list_filter = ('rating', 'date', 'course')
    search_fields = ('student__full_name', 'course__title', 'comment')
    date_hierarchy = 'date'

    def show_comment(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    show_comment.short_description = 'Sharh'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'short_text')
    list_filter = ('created_at',)


# Qolgan modellar uchun sodda ro'yxatdan o'tkazish
admin.site.register(Category)
admin.site.register(Level)
admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Order)
