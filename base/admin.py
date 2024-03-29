from django.contrib import admin
from base.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Specialty)
admin.site.register(Expertise)
admin.site.register(Education)
admin.site.register(HonorsAndAwards)
admin.site.register(Affiliation)
# admin.site.register(Article)
admin.site.register(Keyword)
admin.site.register(ArticleType)
admin.site.register(Institution)
admin.site.register(Resources)



def duplicate_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None  # Set primary key to None to create a new entry
        obj.save()

duplicate_selected.short_description = "Duplicate selected entries"

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = [duplicate_selected]