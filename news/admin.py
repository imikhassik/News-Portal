from django.contrib import admin
from .models import Post, Category


def update_rating(modeladmin, request, queryset):
    queryset.update(rating=10)
update_rating.short_description = 'Задать рейтинг 10'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('type', 'created_on', 'title', 'rating', 'get_categories')
    list_filter = ('type',)
    search_fields = ('title', 'categories__name',)
    actions = [update_rating]

    @staticmethod
    def get_categories(obj):
        return ', '.join(category.name for category in obj.categories.all())


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
