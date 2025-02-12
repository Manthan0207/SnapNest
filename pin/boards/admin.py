from django.contrib import admin

# Register your models here.
from .models import Image
from .models import UserProfile,Like,SavedPin,Notification,Report
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(SavedPin)
admin.site.register(Notification)
admin.site.register(Report)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('user', 'follow_count', 'follower_count', 'monthly_views', 'post_count', 'bio')

    # Add search functionality for the user field
    search_fields = ('user__username',)

    # Enable filtering options for certain fields
    list_filter = ('follow_count', 'follower_count', 'monthly_views', 'post_count')
