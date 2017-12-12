from django.contrib import admin

from .models import waterMark

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','created','modified','title', 'description','image')

admin.site.register(waterMark, ItemAdmin)
