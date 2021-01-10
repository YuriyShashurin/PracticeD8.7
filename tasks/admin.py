from django.contrib import admin

from tasks.models import TodoItem, Category, PriorityCount


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created', 'pk', 'was_priority')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'todos_count')

@admin.register(PriorityCount)
class PriorityCountAdmin(admin.ModelAdmin):
    list_display = ('title', 'count')
