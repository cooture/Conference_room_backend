from django.urls import path
from management.views import user_func, room_func

urlpatterns = [
    path('test/', user_func.test),
    path('getallusers/', user_func.getAllUsers),
    path('getsomeone/', user_func.getSomeone),
    path('searchsomebody/', user_func.searchSomebody),
    path('updateuser/', user_func.updateSomeone),
    path('getusermeeting/', user_func.getUserMeeting),
    path('addupdateusers/', user_func.addUsers),

    path('getallrooms/', room_func.getAllRoom),
    path('searchrooms/', room_func.searchRoom),
    path('addupdaterooms/', room_func.addRooms),


]
