from django.shortcuts import render

# Create your views here.
from .models import ImgModel

def displayAllPaint(request):
    img_models=ImgModel.objects.all()
    body={}
    body['imgs']=img_models

    return render(request,'all_paint.html',body)

