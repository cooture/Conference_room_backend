from time import timezone

from django.db import models


# Create your models here.
class user(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=20, null=False, blank=False)
    sex = models.IntegerField(choices=((0, '男'), (1, '女')), default=0, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    position = models.CharField(max_length=50, null=False, blank=False)
    addtime = models.DateTimeField(auto_now_add=True)
    edittime = models.DateTimeField(auto_now=True)
    passwd = models.CharField(max_length=200, null=False, default="123456")
    pic = models.ImageField(upload_to='static/facelib', default='null')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class room(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=200, null=False, blank=False)
    comment = models.TextField(max_length=500, default="备注为空", null=True, blank=True)
    addtime = models.DateTimeField(auto_now_add=True)
    edittime = models.DateTimeField(auto_now=True)
    manager = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "会议室"
        verbose_name_plural = verbose_name


class meeting(models.Model):
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    theme = models.CharField(max_length=200, null=False, blank=False)
    comment = models.TextField(max_length=1000, null=True, blank=True, default="备注为空")
    person = models.ManyToManyField(user, through='meeting_user_rel', verbose_name="会议人员", related_name='person')
    creat_person = models.ForeignKey(user, on_delete=models.SET_NULL, related_name='creat_person',
                                     null=True, blank=True, verbose_name="管理员")
    room = models.ForeignKey(room, on_delete=models.CASCADE)
    addtime = models.DateTimeField(auto_now_add=True)
    edittime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = "会议"
        verbose_name_plural = verbose_name
        ordering = ['starttime']


class meeting_user_rel(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    meeting = models.ForeignKey(meeting, on_delete=models.CASCADE)
    check = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name + "的" + self.meeting.theme

    class Meta:
        verbose_name = "签到信息"
        verbose_name_plural = verbose_name
        unique_together = (("user", "meeting"))
