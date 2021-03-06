import os
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import markdown


CUR_PATH=os.path.dirname(__file__)
STATIC_PATH=os.path.join(CUR_PATH,"../static")
DOCUMENT_PATH=os.path.join(STATIC_PATH,"documents")
COLORS=["#81c784", "#4caf50","#388e3c","#1b5e20",   # green
        "#ffd54f","#ffc107","#ffa000", "#ff6f00",
        "#5b7fa7","#50bda3","#a4def1","#d06270",
        "#3498db","#34495e","#27ae60","#8e44ad",
        "#3498db","#34495e","#27ae60","#8e44ad",
        "#3498db","#34495e","#27ae60","#8e44ad"]


def displayHome(request):
    body={}
    body['categorys']=[]
    categorys=os.listdir(DOCUMENT_PATH)
    for index,category in enumerate(categorys):
        if category.startswith(".") or (not os.path.isdir(os.path.join(DOCUMENT_PATH,category))):
            continue
        category=category.replace('_','')
        if index > len(COLORS) -1:
            continue
        cat_info={'name':category,'color':COLORS[index]}
        body['categorys'].append(cat_info)
    
    body['categorys'].sort(key=sortName)
    return render(request, 'home.html',body)

def sortName(item):
    return item['name']

def replaceImgUrl(text,category):
    index=category.rfind('/')
    category=category[0:index]

    # 静态图片路径需要带static
    return re.sub(r'''src="(imgs|pics)/(.*?)"''','''src="/static/documents/'''+category+'''/\\1/\\2"''',text,re.S)

def readPostInfo(md_text, article_dir):
    article_title=article_dir
    apos=article_dir.find("/")
    if apos > -1:
        article_title=article_dir[apos+1:]


    info={'title':article_title,'date':'2000-01-01'}
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
    


# display files in category
def categoryView(request,category_name):
    print(category_name)
    body={}
    cate=os.listdir(DOCUMENT_PATH)
    categorys=[]
    for ca in cate:
        pa=os.path.join(DOCUMENT_PATH,ca)
        if os.path.isdir(pa) and (not ca.startswith('.')):
            categorys.append(ca)
    if category_name in categorys:
        categorys=[category_name]
    body['categorys']=[]
    for category in categorys:
        
        cat_dict={}
        cat_dict['name']=category
        cat_dict['files']=[]
        for file_name in os.listdir(os.path.join(DOCUMENT_PATH,category)):
            if  file_name.endswith('.md'):
                cat_dict['files'].append(file_name)
        cat_dict['files'].sort()
        
        body['categorys'].append(cat_dict)

    # 按name排序
    body['categorys'].sort(key=sortName)
    return render(request, 'category.html',body)

def postView(request,article_dir):
    dirs=os.path.join(DOCUMENT_PATH,article_dir+".md")
    text=''
    info={}
    if os.path.exists(dirs):
        with open(dirs,'r',encoding='utf-8') as file:
            text,info=readPostInfo(file.read(),article_dir)
    
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

