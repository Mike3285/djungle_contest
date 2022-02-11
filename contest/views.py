import datetime
import json

from django.shortcuts import render
from django.utils import timezone
from contest import models

from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils.crypto import get_random_string
from django.db.models import ObjectDoesNotExist
from django.contrib.auth import authenticate, login


def check_contest(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error":
                {
                    "status": "403",
                    "title": "Unauthorized",
                    "detail": "You must be logged in to access this resource"
                }
            },
            status=403
        )
    else:
        code = request.GET.get('contest')
        user_id = request.GET.get('user')
        if code and user_id:
            now_datetime = timezone.now().date()
            request_time = datetime.datetime.now()
            try:
                contest = models.Contest.objects.get(code__iexact=code)
            except ObjectDoesNotExist:
                return JsonResponse(
                    {"error": {
                        "status": "404",
                        "title": "Contest not found",
                        "detail": f"Contest code {code} not found."
                    }}, status=404
                )
            if not contest.start_date <= now_datetime <= contest.stop_date:
                return JsonResponse(
                    {
                        "error": {
                            "status": "422",
                            "title": "Contest is not active",
                            "detail": "The contest with code %s is not active." % code
                        }
                    }, status=422
                )
            else:
                user = models.Utente.objects.get(pk=user_id)
                if user in contest.allowed_users.all():
                    winner = check_winner(contest.prize_field, request_time)
                    if winner:
                        return JsonResponse(
                            {
                                "data": {
                                    "winner": winner,
                                    "prize": {
                                        "code": contest.prize_field.code,
                                        "name": contest.prize_field.name
                                    },
                                }
                            }
                        )
                    else:
                        return JsonResponse(
                            {
                                "data": {
                                    "winner": winner,
                                    "prize": None,
                                }
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            "error": {
                                "status": "403",
                                "title": "Forbidden",
                                "detail": "You can't play in this contest"
                            }
                        }, status=403
                    )
        else:
            return JsonResponse(
                {
                    "error": {
                        "status": "400",
                        "title": "Bad request",
                        "detail": 'One of the required parameters "code" or "user_id" are missing'
                    }
                }, status=400
            )


def check_winner(prize, request_time):
    winning_moments = json.loads(prize.winning_timestamps)
    for i in winning_moments.keys():
        date_object = datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f")
        if request_time >= date_object and not winning_moments[i] and prize.won_today <= prize.perday:
            winning_moments[i] = request_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            prize.winning_timestamps = json.dumps(winning_moments)
            prize.won_today += 1
            prize.save()
            return True
    return False


def create_user(request):
    password = request.GET.get('password')
    if password is None:
        return JsonResponse(
            {
                "error": {
                    "status": "400",
                    "title": "Bad request",
                    "detail": 'Required parameter "password" is missing'
                }
            }, status=400
        )
    if not request.user.is_authenticated:
        user = models.Utente.objects.create_user(
            username=get_random_string(length=32),
            password=password,
        )
        return JsonResponse(
            {"data": {
                "status": "201",
                "title": "User Created",
                "your_token": user.username,
                "message": f"Hello! This is your unique token. Please use it to make authenticated requests",
                "your_login_url": f"/login?token={user.username}&password=your-password"
            }}, status=201
        )
    else:
        return JsonResponse(
            {
                "error": {
                    "status": "409",
                    "title": "User already logged",
                    "detail": "You are already logged in"
                }
            }, status=409
        )


def login_user(request):
    token = request.GET.get('token')
    password = request.GET.get('password')
    if token and password:
        # test token:        token=JyfyLyML1WAmxDtK6uIWYW7srhxkm8BH pass=ciao1
        user = authenticate(request, username=token, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(
                {
                    "data": {
                        "status": "200",
                        "title": "Logged in",
                        "detail": 'You are now successfully logged in! Play the contest you want by visiting /play/?<code>'
                    }
                }, status=200
            )
        else:
            return JsonResponse(
                {
                    "error": {
                        "status": "422",
                        "title": "Unprocessable entity",
                        "detail": 'Credentials you provided are wrong'
                    }
                }, status=400
            )

    else:
        return JsonResponse(
            {
                "error": {
                    "status": "400",
                    "title": "Bad request",
                    "detail": 'One of the required parameters "token" or "password" are missing'
                }
            }, status=400
        )
