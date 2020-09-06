import os
import re
import hashlib
import hmac
from hashlib import sha1
import json
import subprocess

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes
from django.views.decorators.http import require_POST




CUR_PATH=os.path.dirname(__file__)
STATIC_PATH=os.path.join(CUR_PATH,"../static")
DOCUMENT_PATH=os.path.join(STATIC_PATH,"documents")

@require_POST  # receive post only
@csrf_exempt  # this is needed
def github_hello(request):
    '''
    for security, we have to make sure:
        1. thr seceret key is correct
    '''
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    if header_signature is None:
        return HttpResponseForbidden('Permission denied.')

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return HttpResponseServerError('Operation not supported.', status=501)

    mac = hmac.new(force_bytes(settings.GITHUB_WEBHOOK_KEY), msg=force_bytes(request.body), digestmod=sha1)
    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return HttpResponseForbidden('Permission denied.')

    payload={}
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
    else:
        payload = json.loads(request.body)
    if "repository" not in payload:
        return HttpResponse('unvalid repository hook')

    repo=payload["repository"]["name"]
    cd_path=''
    if repo=='YeeKal.github.io':
        cd_path=os.path.join(DOCUMENT_PATH)
    elif repo=='BlogYee':
        cd_path=os.path.join(CUR_PATH,"../.")
    else:
        return HttpResponse('unvalid repository name')
    # Process the GitHub events
    event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')
    if event == 'ping':
        return HttpResponse('ping')
    elif event == 'push':
        cd_docu="cd %s"%(cd_path,)+ " &&" +'''echo "%s" &&'''%(cd_path,)
        cmd=cd_docu + \
            '''echo "update from github"  &&''' + \
            '''git fetch origin master &&''' +\
            '''git merge origin/master &&''' +\
            '''git rebase origin/master &&''' +\
            '''echo "update completed!" '''
        subprocess.call(cmd,shell=True)

        return HttpResponse('update success')

    return HttpResponse('pong')

def handle_webhook(event, payload):
    """Simple webhook handler that prints the event and payload to the console"""
    print('Received the {} event'.format(event))
    print(json.dumps(payload, indent=4))


@csrf_exempt
def handle_github_hook(request):
    print("http user agent",request.META)
    # Check the X-Hub-Signature header to make sure this is a valid request.
    github_signature = request.META['HTTP_X_HUB_SIGNATURE']
    signature = hmac.new(settings.GITHUB_WEBHOOK_SECRET, request.body, hashlib.sha1)
    expected_signature = 'sha1=' + signature.hexdigest()
    if not hmac.compare_digest(github_signature, expected_signature):
        return HttpResponseForbidden('Invalid signature header')

    # Sometimes the payload comes in as the request body, sometimes it comes in
    # as a POST parameter. This will handle either case.
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
    else:
        payload = json.loads(request.body)

    event = request.META['HTTP_X_GITHUB_EVENT']

    # This is where you'll do something with the webhook
    handle_webhook(event, payload)

    return HttpResponse('Webhook received')