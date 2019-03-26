from django.urls import path
from management.views import user_func, room_func, meeting_func

urlpatterns = [
    path('test/', user_func.test),
    path('getallusers/', user_func.getAllUsers),
    path('getsomeone/', user_func.getSomeone),
    path('searchsomebody/', user_func.searchSomebody),
    path('updateuser/', user_func.updateSomeone),
    path('getusermeeting/', user_func.getUserMeeting),
    path('addupdateusers/', user_func.addUsers),
    path('logincheck/', user_func.loginCheck),
    path('getfaceliblist/', user_func.getFaceLibList),

    path('getallrooms/', room_func.getAllRoom),
    path('searchrooms/', room_func.searchRoom),
    path('addupdaterooms/', room_func.addRooms),
    path('getroom/', room_func.getroom),
    path('getroommeeting/', room_func.getRoomMeeting),
    path('checkroomtimes/', room_func.checkroomtimes),
    path('nowempty/', room_func.nowempty),
    path('sometimeempty/', room_func.sometimeEmpty),

    path('getallmeeting/', meeting_func.getallmeeting),
    path('getmeeting/', meeting_func.getmeeting),
    # path('searchmeetings/', meeting_func.searchmeetings)
    path('getmeetingperson/', meeting_func.getmeetingperson),
    path('addusermeeting/', meeting_func.addUserMeeting),
    path('usermeetingcheckin/', meeting_func.checkin),
    path('addmeeting/', meeting_func.addmeeting)
]
