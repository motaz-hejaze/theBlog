from django.contrib import admin
from .models import Post,Comment,Mailer
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    # list_display for the list of posts view
    list_filter = ('status' , 'created', 'publish' , 'author')
    # right side bar for filters
    search_fields = ('title' , 'body')
    # a search text input
    prepopulated_fields = {'slug':('title',)}
    #populate slug from title text replacing spaces with -
    raw_id_fields = ('author',)
    # looking for objects using id number
    date_hierarchy = 'publish'
    # a day go links under the search bars
    ordering = ['status','publish']
    # ordering possibility for a column
admin.site.register(Post,PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name' , 'email' , 'post' , 'created' , 'active')
    list_filter = ('active' , 'created' , 'updated')
    search_fields = ('name' , 'email' , 'body')
admin.site.register(Comment,CommentAdmin)

@admin.register(Mailer)
class MailerAdmin(admin.ModelAdmin):

    # some code...

    def has_add_permission(self, request):
        # check if generally has add permission
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and Mailer.objects.exists():
            retVal = False
        return retVal