import django
from django.contrib import admin
from . import models
# Register your models here.

class rel(admin.TabularInline):
    model = models.meeting_user_rel

class meeting_rel(admin.TabularInline):
    model = models.meeting


class useradmin(admin.ModelAdmin):
    inlines = [rel]
    search_fields = ('name','id',)
    list_filter = ('sex','position')
    list_display = ('id', 'name', 'sex','email','position')

class meetingadmin(admin.ModelAdmin):
    search_fields = ('theme',)
    inlines = [rel]
    list_display = ('theme', 'starttime', 'endtime', 'room', 'comment')

class roomadmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = [meeting_rel]
    list_display = ('id', 'name', 'location', 'type', 'manager', 'comment')


admin.sites.AdminSite.site_title = "智能会议室后台"
admin.sites.AdminSite.site_header = "智能会议室后台"
admin.sites.AdminSite.index_title = "智能会议室后台"
admin.site.register(models.user, useradmin)
admin.site.register(models.room, roomadmin)
admin.site.register(models.meeting, meetingadmin)
# admin.site.register(models.meeting_user_rel)