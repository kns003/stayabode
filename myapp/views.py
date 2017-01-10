import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import UserProfile
from datetime import datetime

MESSAGE = 'message'
SENDER = 'sender'
ROLE = 'role'
STATUS = 'status'
SUCCESS = 'success'
BROADCASTS = 'broadcasts'
GREETING = 'greeting'
USER = 'user'
EXCLAMATORY_MARK = '!'
DATA = 'data'
MORNING_GREETING = 'Morning'
INDENT_SPACE = 4
JSON_CONTENT_TYPE = "application/json"
DATE_FORMAT = '%Y-%m-%d'
ERROR = 'error'

# Create your views here.
def broadcasts(request):
    if request.method == 'GET':
        try:
            logged_user = UserProfile.objects.get(user=request.user)
        except Exception as e:
            return HttpResponse(json.dumps({STATUS: ERROR, "message": "No user Found"}))
        user_email = request.GET.get('email', '')
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', '')
        
        if date_from and date_to:
            if user_email:
                user_objs = UserProfile.objects.filter(
                    user__email=user_email,
                    broadcast__created_at__range=(datetime.strptime(date_from, DATE_FORMAT),
                                                  datetime.strptime(date_to, DATE_FORMAT)))
            else:
                user_objs = UserProfile.objects.all(
                    broadcast__created_at__range=(datetime.strptime(date_from, DATE_FORMAT),
                                                  datetime.strptime(date_to, DATE_FORMAT)))
        else:
            if user_email:
                user_objs = UserProfile.objects.filter(user__email=user_email)
            else:
                user_objs = UserProfile.objects.all()
                
        json_list = []
        for user_obj in user_objs:
            tmp_dict = dict()
            if bool(user_obj.broadcasts):
            
                tmp_dict[MESSAGE] = user_obj.broadcasts.message + ' on ' + user_obj.broadcasts.date.strftime('%A,'
                                                                                                           '%d %I %p')
                tmp_dict[SENDER] = user_obj.user.first_name
                tmp_dict[ROLE] = user_obj.role
            json_list.append(tmp_dict)
            
        response = {STATUS: SUCCESS,
                    DATA: {BROADCASTS: json_list,
                           GREETING: MORNING_GREETING + request.user.first_name + EXCLAMATORY_MARK,
                           USER: logged_user.as_json()}}
        return HttpResponse(json.dumps(response, indent=INDENT_SPACE), content_type=JSON_CONTENT_TYPE)