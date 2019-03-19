from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from .models import user, meeting, room

# Create your views here.

method_key = ['1']


def makeUserInfo(i_users):
    user_data = {'user_id': i_users.id, 'name': i_users.name, 'sex': i_users.get_sex_display(), 'email': i_users.email,
                 'phone': i_users.phone,
                 'postion': i_users.position, 'add_time': i_users.addtime, 'edit_time': i_users.edittime}
    return user_data


def makeMeetingInfo(i_meeting):
    meeting_data = {'theme': i_meeting.theme, 'comment': i_meeting.comment, 'start_time': i_meeting.starttime,
                    'end_time': i_meeting.endtime, 'creat_person': i_meeting.creat_person.name,
                    'creat_person_id': i_meeting.creat_person.id, 'room_name': i_meeting.room.name,
                    'room_name_id': i_meeting.room.id}
    return meeting_data


def makeRoomInfo(i_room):
    room_data = {'room_id': i_room.id, 'name': i_room.name, 'location': i_room.location, 'type': i_room.type,
                 'comment': i_room.comment, 'manager_id': i_room.manager_id, 'manager': i_room.manager.name}
    return room_data


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
        :param:key, sid
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
                sid = request_data['sid']
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
                    data['status'] = 602
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
                        print(e)

            else:
                data['status'] = 602
                data['info'] = 'error key'

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

    def searchRoom(requset):
        """

        :return:
        """
        data = {
            'status': 210,
            'info': 'search rooms',
            'data': []
        }
        if requset.method == 'POST':
            if 'key' in requset.POST.keys():
                if requset.POST['key'] in method_key:
                    post_data = requset.POST

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
                        room.objects.update_or_create(id=post_data['rid'],
                                                      defaults={'name': post_data['name'], 'type': post_data['type'],
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



class web(View):
    def test(requset):
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
