from django.contrib import admin

# Register your models here.
from .models import Profile,vedios,Comment,communitypost,community_comment,Support,groups,gourpskills,test

# Register your models here.

admin.site.register(Profile)
admin.site.register(vedios)
admin.site.register(Comment)
admin.site.register(communitypost)
admin.site.register(community_comment)
admin.site.register(Support)
admin.site.register(groups)
admin.site.register(gourpskills)
admin.site.register(test)