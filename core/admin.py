from django.contrib import admin
from .models import Banner, SuccessStudent, NoticeBoard

admin.site.site_header = "Raju Math Administration"
admin.site.site_title = "Raju Math Admin Portal"
admin.site.index_title = "Welcome to Raju Math Administration"

admin.site.register(Banner)
admin.site.register(SuccessStudent)
admin.site.register(NoticeBoard)