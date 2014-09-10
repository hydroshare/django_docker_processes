from . import models, signals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def process_finished(request, profile_name, token, *args, **kwargs):
    profile = get_object_or_404(models.DockerProfile, name=profile_name)
    proc = get_object_or_404(models.DockerProcess, profile__name=profile_name, token=token)
    proc.delete()

    signals.process_completed(models.DockerProfile,
          profile,
          token=token,
          result_text=request.POST.get('result_text', None),
          result_data=json.loads(request.POST.get('result_data', [])) if 'result_data' in request.POST else None,
          result_files=request.FILES
    )
    return HttpResponse()

@csrf_exempt
def process_aborted(request, profile_name, token, *args, **kwargs):
    profile = get_object_or_404(models.DockerProfile, name=profile_name)
    proc = get_object_or_404(models.DockerProcess, profile__name=profile_name, token=token)
    proc.delete()

    signals.process_aborted(models.DockerProfile,
          profile,
          token=token,
          error_text=request.POST.get('error_text', None),
          error_data=json.loads(request.POST.get('error_data', [])) if 'result_data' in request.POST else None
    )
    return HttpResponse()

