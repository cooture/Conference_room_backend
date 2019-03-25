from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.test import ignore_warnings
from django.utils.datetime_safe import datetime
from django.views.generic import View

from .models import user, meeting, room, meeting_user_rel

# Create your views here.

method_key = ['1']


def makeUserInfo(i_users):
    user_data = {'user_id': i_users.id, 'name': i_users.name, 'sex': i_users.get_sex_display(), 'email': i_users.email,
                 'phone': i_users.phone,
                 'postion': i_users.position, 'add_time': i_users.addtime, 'edit_time': i_users.edittime}
    return user_data


def makeMeetingInfo(i_meeting):
    meeting_data = {'id': i_meeting.id, 'theme': i_meeting.theme, 'comment': i_meeting.comment,
                    'start_time': i_meeting.starttime,
                    'end_time': i_meeting.endtime, 'creat_person': i_meeting.creat_person.name,
                    'creat_person_id': i_meeting.creat_person.id, 'room_name': i_meeting.room.name,
                    'room_name_id': i_meeting.room.id}
    return meeting_data


def makeRoomInfo(i_room):
    room_data = {'room_id': i_room.id, 'name': i_room.name, 'location': i_room.location, 'type': i_room.type,
                 'comment': i_room.comment, 'manager_id': i_room.manager_id, 'manager': i_room.manager.name}
    return room_data


def makeMeetingPersonRela(i):
    return {'user_id': i.user.id, 'user_name': i.user.name, 'meeting_id': i.meeting.id,
            'meeting_theme': i.meeting.theme, 'check': i.check}


def getTimeFromStr(str):
    getdate = str.split()[0].split('-')
    gettime = str.split()[1].split(':')
    year = int(getdate[0])
    month = int(getdate[1])
    day = int(getdate[2])
    hour = int(gettime[0])
    min = int(gettime[1])
    sec = int(gettime[2])
    # datetime.datetime(2019, 3, 22, 23, 51, 51)
    # return year, month, day, hour, min, sec
    return datetime(year, month, day, hour, min, sec)


class user_func(View):
    def test(request):
        """
        :comment:test gen method
        :method:GET
        :url:/gen/test
        :return: HttpResponse
        """
        return HttpResponse("This is gen test", status=202)

    def getAllUsers(request):
        """
        :comment:get all users
        :url:/gen/getallusers
        :method:POST
        :param:key
        :return: json
        :errcode_601: error key
        :errcode_602: something error
        :errcode_603: error method
        """
        data = {
            "status": int,
            "info": "all_users",
            "data": [],
        }
        if request.method == 'POST':
            try:
                if request.POST['key'] not in method_key:
                    data['status'] = 601
                    data['info'] = "error key"
                else:
                    users = user.objects.all().order_by('-edittime')
                    for i_users in users:
                        data['data'].append(makeUserInfo(i_users))
                    data['status'] = 210
            except:
                data['status'] = 602
                data['info'] = 'something error'
        else:
            data['status'] = 603
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    def getSomeone(request):
        """
        :method:post
        :param:key, uid
        :url:/gen/getsomeone
        :return: json
        :errcode_601: 非法请求
        :errcode_602: 参数错误
        :errcode_603: 查无此人
        :errcode_604: 访问key错误
        """
        data = {
            'status': int,
            'info': str,
            'data': [],

        }
        if request.method == 'POST':
            request_data = request.POST
            try:
                key = request_data['key']
                sid = request_data['uid']
                if key not in method_key:
                    data['status'] = 604
                    data['info'] = "error key"
                else:
                    try:
                        someone = user.objects.get(id=sid)
                        data['data'].append(makeUserInfo(someone))
                        data['info'] = 'getSomeone info'
                        data['status'] = 210
                    except:
                        data['info'] = 'cannot search someone'
                        data['status'] = 603  # TODO:603查无此人


            except:
                data['status'] = 602  # TODO：602参数错误或无法解析参数
                data['info'] = "error params"
                data['data'].clear()

        else:
            data['status'] = 601
            data['info'] = "error method"  # TODO：非法请求

        return JsonResponse(data, safe=False, status=200)

    def searchSomebody(request):
        """

        :url:/gen/searchsomebody/
        :param:key, [name, sex, email, position, phone]at least one
        :method:POST
        :errcode_601: error method
        :errcode_602: error key
        :return:
        """
        data = {
            'status': 210,
            'info': "search somebody",
            'data': [],
        }
        if request.method == 'POST':
            if 'key' in request.POST.keys():
                if request.POST['key'] not in method_key:
                    data['status'] = 603
                    data['info'] = 'error key'

                else:

                    post_data = request.POST
                    name = ''
                    sex = 0
                    email = ''
                    position = ''
                    phone = ''

                    if 'name' in post_data.keys():
                        name = post_data['name']
                        pass
                    if 'sex' in post_data.keys():
                        sex = int(post_data['sex'])
                        pass
                    if 'email' in post_data.keys():
                        email = post_data['email']
                        pass
                    if 'position' in post_data.keys():
                        position = post_data['position']
                        pass
                    if 'phone' in post_data.keys():
                        phone = post_data['phone']
                        pass

                    try:
                        somebody = user.objects.filter(name__contains=name, sex__gte=sex, email__contains=email,
                                                       position__contains=position, phone__contains=phone)
                        for i_somebody in somebody:
                            data['data'].append(makeUserInfo(i_somebody))

                        data['status'] = 210
                        data['info'] = 'search somebody'
                        pass
                    except Exception as e:
                        # print(e)
                        data['status'] = 604
                        data['info'] = str(e)

            else:
                data['status'] = 602
                data['info'] = 'error param'

        else:
            data['status'] = 601
            data['info'] = "error method"

        return JsonResponse(data, safe=False)

    def updateSomeone(requsest):
        """
        :url:/updateuse/
        :param: key, uid, [name, sex, email, position, phone]
        :errcode_601:error method
        :errcode_602:error param
        :errcode_603:error key
        :errcode_604:cannot find user
        :errcode_605:update error
        :return: json
        """
        data = {
            'status': 210,
            'info': 'update someone',
            'data': []
        }
        if requsest.method == 'POST':
            if 'key' and 'uid' in requsest.POST.keys():
                if requsest.POST['key'] in method_key:

                    post_data = requsest.POST
                    try:
                        get_user = user.objects.get(id=post_data['uid'])
                        name = get_user.name
                        sex = get_user.sex
                        email = get_user.email
                        position = get_user.position
                        phone = get_user.phone
                    except Exception as e:
                        data['status'] = 604
                        data['info'] = str(e)
                        return JsonResponse(data, safe=False)

                    if 'name' in post_data.keys():
                        name = post_data['name']
                        pass
                    if 'sex' in post_data.keys():
                        sex = int(post_data['sex'])
                        pass
                    if 'email' in post_data.keys():
                        email = post_data['email']
                        pass
                    if 'position' in post_data.keys():
                        position = post_data['position']
                        pass
                    if 'phone' in post_data.keys():
                        phone = post_data['phone']
                        pass

                    try:
                        user.objects.filter(id=post_data['uid']).update(name=name, sex=sex, email=email,
                                                                        position=position, phone=phone)
                        data['data'].append(makeUserInfo(user.objects.get(id=post_data['uid'])))
                        data['info'] = "succeed update uid:" + str(post_data['uid'])
                    except Exception as e:
                        print(e)
                        data['status'] = 605
                        data['info'] = str(e)
                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = "error param"
            pass
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    def getUserMeeting(request):
        """
        :param:key,uid
        :url:/getusermeeting/
        :errcode_601: error method
        :return:json
        """
        data = {
            'status': 210,
            'info': 'get user metting',
            'user': {},
            'data': []
        }
        if request.method == 'POST':
            if 'key' and 'uid' in request.POST.keys():
                if request.POST['key'] in method_key:
                    try:
                        data['user'] = makeUserInfo(user.objects.get(id=request.POST['uid']))
                        user_metting = user.objects.get(id=request.POST['uid']).person.all()
                        for i_meeting in user_metting:
                            data['data'].append(makeMeetingInfo(i_meeting))
                            data['info'] = 'success get user meeting'
                    except Exception as e:
                        data['status'] = 604
                        data['info'] = str(e)
                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = 'error param'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    def addUsers(request):
        data = {
            'status': 201,
            'info': "add users",
            'data': []
        }
        if request.method == 'POST':
            if 'key' and 'uid' and 'name' and 'sex' and 'phone' and 'email' and 'position' in request.POST.keys():
                if request.POST['key'] in method_key:
                    post_data = request.POST

                    try:
                        user.objects.update_or_create(id=post_data['uid'],
                                                      defaults={'name': post_data['name'], 'sex': int(post_data['sex']),
                                                                'phone': post_data['phone'],
                                                                'email': post_data['email'],
                                                                'position': post_data['position']})

                        succ_add = user.objects.get(id=post_data['uid'])
                        data['data'].append(makeUserInfo(succ_add))
                        data['info'] = 'succeed add or update users'
                    except Exception as e:
                        # print(e)
                        data['status'] = 604
                        data['info'] = str(e)


                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = 'error param'
        else:
            data['status'] = 601
            data['info'] = 'error method'
        return JsonResponse(data, safe=False)


class room_func(View):
    def test(request):
        return HttpResponse('this is room_func test')

    def getAllRoom(request):
        data = {
            'status': 210,
            'info': 'get all rooms',
            'data': []
        }
        if request.method == 'POST':
            if 'key' in request.POST.keys():
                if request.POST['key'] in method_key:
                    try:
                        all_rooms = room.objects.all()

                        for i_room in all_rooms:
                            data['data'].append(makeRoomInfo(i_room))
                        data['status'] = 210
                        data['info'] = 'succeed return all rooms'
                    except Exception as e:
                        data['status'] = 604
                        data['info'] = str(e)

                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = 'error parma'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    def searchRoom(request):
        """

        :return:
        """
        data = {
            'status': 210,
            'info': 'search rooms',
            'data': []
        }
        if request.method == 'POST':
            if 'key' in request.POST.keys():
                if request.POST['key'] in method_key:
                    post_data = request.POST

                    name = ''
                    location = ''
                    type = ''
                    manager = ''
                    # if 'rid' in post_data.keys():
                    #     id = post_data['rid']
                    if 'name' in post_data.keys():
                        name = post_data['name']
                    if 'location' in post_data.keys():
                        location = post_data['location']
                    if 'type' in post_data.keys():
                        type = post_data['type']
                    if 'manager' in post_data.keys():
                        manager = post_data['manager']
                    try:
                        search_res = room.objects.filter(name__contains=name, location__contains=location,
                                                         type__contains=type, manager__name__contains=manager)
                        for i_room in search_res:
                            data['data'].append(makeRoomInfo(i_room))
                    except Exception as e:
                        data['status'] = 604
                        data['info'] = str(e)
                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = 'error parma'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    def addRooms(request):
        data = {
            'status': 210,
            'info': 'add rooms',
            'data': []
        }
        if request.method == 'POST':
            if 'key' and 'rid' and 'name' and 'type' and 'location' and 'manager_id' in request.POST.keys():
                if request.POST['key'] in method_key:
                    post_data = request.POST

                    try:
                        if 'comment' in post_data.keys():
                            room.objects.update_or_create(id=post_data['rid'],
                                                          defaults={'name': post_data['name'],
                                                                    'type': post_data['type'],
                                                                    'location': post_data['location'],
                                                                    'manager_id': post_data['manager_id'],
                                                                    'comment': post_data['comment']})

                        else:
                            room.objects.update_or_create(id=post_data['rid'],
                                                          defaults={'name': post_data['name'],
                                                                    'type': post_data['type'],
                                                                    'location': post_data['location'],
                                                                    'manager_id': post_data['manager_id']})

                        succ_add = room.objects.get(id=post_data['rid'])
                        data['data'].append(makeRoomInfo(succ_add))
                        data['info'] = 'succeed add or update rooms'
                    except Exception as e:
                        # print(e)
                        data['status'] = 604
                        data['info'] = str(e)


                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = 'error param'
        else:
            data['status'] = 601
            data['info'] = 'error method'
        return JsonResponse(data, safe=False)

    def getRoomMeeting(request):
        data = {
            'status': 210,
            'info': 'get rooms meeting info',
            'data': []

        }
        if request.method == 'POST':
            if 'key' and 'rid' in request.POST.keys():
                if request.POST['key'] in method_key:
                    post_data = request.POST
                    try:
                        search = room.objects.get(id=post_data['rid']).meeting_set.all().order_by('-starttime')
                        for i_meeting in search:
                            data['data'].append(makeMeetingInfo(i_meeting))
                        data['info'] = 'succeed search'
                    except Exception as e:
                        data['status'] = 604
                        data['info'] = str(e)
                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['info'] = 'error param'
                data['status'] = 602
        else:
            data['status'] = 601
            data['info'] = 'error method'
        return JsonResponse(data, safe=False)

    def getroom(request):
        data = {
            'status': 210,
            'info': "get all meeting",
            'data': [],
        }
        if request.method == 'POST':
            if 'key' and 'rid' in request.POST.keys():
                if request.POST['key'] in method_key:
                    try:
                        search = room.objects.get(id=request.POST['rid'])

                        data['data'].append(makeRoomInfo(search))
                    except Exception as e:
                        data['status'] = 604
                        data['info'] = str(e)
                else:
                    data['info'] = 'error key'
                    data['status'] = 603
            else:
                data['status'] = 602
                data['info'] = 'error param'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    def checkroomtimes(request):
        data = {
            'status': 210,
            'info': 'check room\'s time',
            'data': []
        }
        if request.method == 'POST':
            if 'key' and 'endtime' and 'rid' and 'starttime' in request.POST.keys():
                if request.POST['key'] in method_key:

                    try:
                        rid = request.POST['rid']
                        start = getTimeFromStr(request.POST['starttime'])
                        end = getTimeFromStr(request.POST['endtime'])
                        res = room.objects.get(id=rid).meeting_set.all()
                        flag = True

                        if start < end:

                            for i_meeting in res:
                                if (start < i_meeting.starttime and end > i_meeting.starttime) or (
                                        start > i_meeting.starttime and end < i_meeting.endtime) or (
                                        start < i_meeting.endtime and end > i_meeting.endtime):
                                    flag = False

                            data['data'].append(flag)
                        else:
                            data['status'] = 605
                            data['info'] = 'error time param'


                    except Exception as e:
                        data['info'] = str(e)
                        data['status'] = 604
                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = 'error parma'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)


class meeting_func(View):
    def getallmeeting(request):
        data = {
            'status': 210,
            'info': "get all meeting",
            'data': [],
        }
        if request.method == 'POST':
            if 'key' in request.POST.keys():
                if request.POST['key'] in method_key:
                    try:
                        search = meeting.objects.all().order_by('-starttime')
                        for i_meeting in search:
                            data['data'].append(makeMeetingInfo(i_meeting))
                    except Exception as e:
                        data['status'] = 604
                        data['info'] = str(e)
                else:
                    data['info'] = 'error key'
                    data['status'] = 603
            else:
                data['status'] = 602
                data['info'] = 'error param'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    def getmeeting(request):
        data = {
            'status': 210,
            'info': "get all meeting",
            'data': [],
        }
        if request.method == 'POST':
            if 'key' and 'mid' in request.POST.keys():
                if request.POST['key'] in method_key:
                    try:
                        search = meeting.objects.get(id=request.POST['mid'])

                        data['data'].append(makeMeetingInfo(search))
                    except Exception as e:
                        data['status'] = 604
                        data['info'] = str(e)
                else:
                    data['info'] = 'error key'
                    data['status'] = 603
            else:
                data['status'] = 602
                data['info'] = 'error param'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    # def searchmeetings(request):
    #     data = {
    #         'status': 210,
    #         'info': 'search meetings',
    #         'data': []
    #     }
    #     if request.method == 'POST':
    #         if 'key' in request.POST.keys():
    #             if request.POST['key'] in method_key:
    #                 post_data = request.POST
    #                 theme = ""
    #                 creat_person = ""

    #
    #             name = ''
    #             location = ''
    #             type = ''
    #             manager = ''
    #             # if 'rid' in post_data.keys():
    #             #     id = post_data['rid']
    #             if 'name' in post_data.keys():
    #                 name = post_data['name']
    #             if 'location' in post_data.keys():
    #                 location = post_data['location']
    #             if 'type' in post_data.keys():
    #                 type = post_data['type']
    #             if 'manager' in post_data.keys():
    #                 manager = post_data['manager']
    #             try:
    # search_res = meeting.objects.filter(starttime__lte=datetime(2019, 3, 22, 23, 20, 2))# 早于该时间的
    # search_res = meeting.objects.filter(starttime__gte='2019-03-22 23:50:51')# 晚于该时间的

    #             except Exception as e:
    #                 data['status'] = 604
    #                 data['info'] = str(e)
    #         else:
    #             data['status'] = 603
    #             data['info'] = 'error key'
    #     else:
    #         data['status'] = 602
    #         data['info'] = 'error parma'
    # else:
    #     data['status'] = 601
    #     data['info'] = 'error method'
    #
    # return JsonResponse(data, safe=False)

    def getmeetingperson(request):
        data = {
            'status': 210,
            'info': 'get meeting person',
            'data': []
        }
        if request.method == 'POST':
            if 'key' and 'mid' in request.POST.keys():
                if request.POST['key'] in method_key:
                    mid = request.POST['mid']
                    try:
                        search = meeting.objects.get(id=mid).meeting_user_rel_set.all()
                        for i_search in search:
                            data['data'].append(makeMeetingPersonRela(i_search))
                    except Exception as e:
                        data['info'] = str(e)
                        data['status'] = 604
                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = 'error parma'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    def addUserMeeting(request):
        data = {
            'status': 210,
            'info': 'add user meeting',
            'data': []
        }
        if request.method == 'POST':
            if 'key' and 'mid' and 'uid' in request.POST.keys():
                if request.POST['key'] in method_key:
                    mid = request.POST['mid']
                    try:
                        mid = request.POST['mid']
                        uid = request.POST['uid']
                        meeting_user_rel(user_id=uid, meeting_id=mid).save()
                        res = meeting.objects.get(id=mid).meeting_user_rel_set.get(user_id=uid)
                        data['data'].append(makeMeetingPersonRela(res))
                    except Exception as e:
                        data['info'] = str(e)
                        data['status'] = 604
                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = 'error parma'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    def checkin(request):
        data = {
            'status': 210,
            'info': 'add user meeting',
            'data': []
        }
        if request.method == 'POST':
            if 'key' and 'mid' and 'uid' in request.POST.keys():
                if request.POST['key'] in method_key:
                    mid = request.POST['mid']
                    try:
                        mid = request.POST['mid']
                        uid = request.POST['uid']
                        res = meeting.objects.get(id=mid).meeting_user_rel_set.get(user_id=uid)
                        if 'check' in request.POST.keys():
                            if request.POST['check'] == '0':
                                res.check = False
                            else:
                                res.check = True
                        else:
                            res.check = True
                        res.save()

                        data['data'].append(makeMeetingPersonRela(res))
                    except Exception as e:
                        data['info'] = str(e)
                        data['status'] = 604
                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = 'error parma'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)

    def addmeeting(request):
        data = {
            'status': 210,
            'info': 'add user meeting',
            'data': []
        }
        if request.method == 'POST':
            if 'key' and 'uid' and 'starttime' and 'endtime' and 'theme' and 'rid' in request.POST.keys():
                if request.POST['key'] in method_key:
                    try:
                        uid = request.POST['uid']
                        starttime = getTimeFromStr(request.POST['starttime'])
                        endtime = getTimeFromStr(request.POST['endtime'])
                        theme = request.POST['theme']
                        rid = request.POST['rid']

                        res = room.objects.get(id=rid).meeting_set.exclude(theme=theme).all()
                        flag = True
                        if starttime < endtime:

                            for i_meeting in res:
                                if (starttime < i_meeting.starttime and endtime > i_meeting.starttime) or (
                                        starttime > i_meeting.starttime and endtime < i_meeting.endtime) or (
                                        starttime < i_meeting.endtime and endtime > i_meeting.endtime):
                                    flag = False

                        if flag:

                            if 'comment' in request.POST.keys():
                                meeting.objects.update_or_create(theme=theme,
                                                                 defaults={'starttime': starttime, 'endtime': endtime,
                                                                           'room_id': rid,
                                                                           'comment': request.POST['comment'],
                                                                           'creat_person_id': uid})
                            else:
                                meeting.objects.update_or_create(theme=theme,
                                                                 defaults={'starttime': starttime, 'endtime': endtime,
                                                                           'room_id': rid, 'creat_person_id': uid})

                            res = meeting.objects.get(theme=theme)
                            data['data'].append(makeMeetingInfo(res))
                        else:
                            data['status'] = 605
                            data['info'] = 'error date param'

                    except Exception as e:
                        data['info'] = str(e)
                        data['status'] = 604
                else:
                    data['status'] = 603
                    data['info'] = 'error key'
            else:
                data['status'] = 602
                data['info'] = 'error parma'
        else:
            data['status'] = 601
            data['info'] = 'error method'

        return JsonResponse(data, safe=False)


class web(View):
    def test(requset):
        a = meeting.objects.exclude(theme="asdasdas").all()
        print(a)
        return HttpResponse("This is web test", status=202)

    def is_online(request):
        data = {
            'status': 202,
            'isrunning': True,
            'data': "Server is running"
        }
        return JsonResponse(data, safe=False)

    def static_test(request):
        return render(request, 'web/index.html')


class android(View):
    def test(request):
        return HttpResponse("this is android test", status=202)
