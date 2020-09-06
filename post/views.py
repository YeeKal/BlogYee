import os
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import markdown


CUR_PATH=os.path.dirname(__file__)
STATIC_PATH=os.path.join(CUR_PATH,"../static")
DOCUMENT_PATH=os.path.join(STATIC_PATH,"documents")
COLORS=["#1abc9c", "#2ecc71","#3498db","#34495e",
        "#27ae60","#8e44ad","#1abc9c", "#2ecc71",
        "#3498db","#34495e","#27ae60","#8e44ad",
        "#3498db","#34495e","#27ae60","#8e44ad"]


def displayHome(request):
    body={}
    body['categorys']=[]
    categorys=os.listdir(DOCUMENT_PATH)
    for index,category in enumerate(categorys):
        if category.startswith("."):
            continue
        category=category.replace('_','')
        cat_info={'name':category,'color':COLORS[index]}
        body['categorys'].append(cat_info)
    return render(request, 'home.html',body)

def replaceImgUrl(text,category):
    index=category.rfind('/')
    category=category[0:index]

    # 静态图片路径需要带static
    return re.sub(r'''src="(imgs|pics)/(.*?)"''','''src="/static/documents/'''+category+'''/\\1/\\2"''',text,re.S)

def readPostInfo(md_text):
    info={'title':'title','date':'2020-09-01'}
    m=re.match(r'---(.*?)---',md_text,re.S)
    if not m:
        return md_text, info
    
    md_text.replace(m.group(),'')
    desc=m.group(1)

    m=re.search(r'title:(.*?)\n',desc)
    if m:
        info['title']=m.group(1).strip()
    
    m=re.search(r'date:(.*?)\n',desc)
    if m:
        info['date']=m.group(1).strip()
    
    return md_text,info
    



def categoryView(request):
    body={}
    cate=os.listdir(DOCUMENT_PATH)
    categorys=[]
    for ca in cate:
        pa=os.path.join(DOCUMENT_PATH,ca)
        if os.path.isdir(pa) and (not ca.startswith('.')):
            categorys.append(ca)
    print(categorys)
    body['categorys']=[]
    for category in categorys:
        
        cat_dict={}
        cat_dict['name']=category
        cat_dict['files']=[]
        for file_name in os.listdir(os.path.join(DOCUMENT_PATH,category)):
            if  file_name.endswith('.md'):
                cat_dict['files'].append(file_name)
        
        body['categorys'].append(cat_dict)

    return render(request, 'category.html',body)

def postView(request,article_dir):
    dirs=os.path.join(DOCUMENT_PATH,article_dir+".md")
    text=''
    info={}
    if os.path.exists(dirs):
        with open(dirs,'r',encoding='utf-8') as file:
            text,info=readPostInfo(file.read())
    
    body={}
    text=markdown.markdown( text,
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    body['content']=replaceImgUrl(text,article_dir)
    body['title']=info['title']
    body['date']=info['date']

    return render(request, 'post.html',body)

def display3d(request):
    return render(request,'view3d.html')

