import datetime
import json

from django.shortcuts import render
from django.utils import timezone
from contest import models

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.db.models import ObjectDoesNotExist
from django.core import serializers


def check_contest(request, code):
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
        winner = check_winner(contest.prize_field, request_time)
        if winner:
            data = json.loads(serializers.serialize('json', [contest.prize_field], fields=('name', 'code')))
            return JsonResponse(
                {
                    "data": {
                        "winner": winner,
                        "prize": data[0],
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


def check_winner(prize, request_time):
    winning_moments = json.loads(prize.winning_timestamps)
    print(winning_moments)
    print(request_time)
    for i in winning_moments.keys():
        date_object = datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f")
        if request_time >= date_object and not winning_moments[i] and prize.won_today <= prize.perday:
            winning_moments[i] = request_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            prize.winning_timestamps = json.dumps(winning_moments)
            prize.won_today += 1
            prize.save()
            return True
    return False