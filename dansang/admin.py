from django.contrib import admin
from .models import DansangInput, DansangSeed, SeedCategory, SeedCategoryEng

class DansangAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(DansangInput)
admin.site.register(DansangSeed, DansangAdmin)
admin.site.register(SeedCategory)
admin.site.register(SeedCategoryEng)