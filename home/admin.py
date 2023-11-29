from django.contrib import admin
from .models import HomeVideo, Comment, BuyModel


# registering the models to admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created")


admin.site.register(HomeVideo)
admin.site.register(Comment, CommentAdmin)
admin.site.register(BuyModel)
