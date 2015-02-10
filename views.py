from . import models, signals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def process_finished(request, profile_name, token, *args, **kwargs):
    """
    View for when a process is finished. When a process is finished, it should
    post to this URL its results.  Any FILES will be passed on to the receiver.
    The other valid parameters are:

    * result_text: arbitrary plain text for results
    * result_data: JSON results to be processed as such on the backend


    :param request:
    :param profile_name:
    :param token:
    :param args:
    :param kwargs:
    :return:
    """
    import logging
    logger = logging.getLogger('django')
    logger.info('process_finished called ...')

    proc = get_object_or_404(models.DockerProcess, profile__name=profile_name, token=token)
    profile = proc.profile
    logs = proc.logs
    if not logs:
        logs = 'No log output from process'
    proc.finished = True
    proc.save()

    logger.info("Logs {0}".format(logs))

    signals.process_finished.send(models.DockerProcess,
          instance=proc,
          token=token,
          result_text=request.POST.get('result_text', None),
          result_data=json.loads(request.POST.get('result_data', [])) if 'result_data' in request.POST else None,
          result_files=request.FILES,
          logs=logs
    )
    return HttpResponse()

@csrf_exempt
def process_aborted(request, profile_name, token, *args, **kwargs):
    """
    View for when a process fails with an error. When a process fails, it should
    post to this URL its results.  The other valid parameters are:

    * error_text: arbitrary plain text for results
    * error_data: JSON results to be processed as such on the backend

    :param request:
    :param profile_name:
    :param token:
    :param args:
    :param kwargs:
    :return:
    """
    import logging
    logger = logging.getLogger('django')
    logger.info('process_aborted called ...')

    proc = get_object_or_404(models.DockerProcess, profile__name=profile_name, token=token)
    profile = proc.profile
    logs = proc.logs
    proc.finished = True
    proc.error = True
    proc.save()

    signals.process_aborted.send(models.DockerProcess,
          instance=proc,
          token=token,
          error_text=request.POST.get('error_text', None),
          error_data=json.loads(request.POST.get('error_data', [])) if 'result_data' in request.POST else None,
          logs=logs
    )
    return HttpResponse()


