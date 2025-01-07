from django.contrib import admin
# Register your models here.
from .models import WeatherPost

@admin.register(WeatherPost)
class WeatherPostAdmin(admin.ModelAdmin):
    list_display = ('location', 'temperature', 'conditions', 'user', 'created_at')
    list_filter = ('created_at', 'conditions')
    search_fields = ('location', 'user__username')
    readonly_fields = ('created_at',)
    
    def get_agree_count(self, obj):
        return obj.agrees.count()
    get_agree_count.short_description = 'Agrees'
    
    def get_disagree_count(self, obj):
        return obj.disagrees.count()
    get_disagree_count.short_description = 'Disagrees'