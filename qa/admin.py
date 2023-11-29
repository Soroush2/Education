from django.contrib import admin
from .models import Answer, Question, Category


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'added_at',)
    search_fields = ('author',)
    list_filter = ('author', 'added_at',)
    ordering = ('id',)


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'added_at', 'question_id')


admin.site.register(Answer, AnswerAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'slug')
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
