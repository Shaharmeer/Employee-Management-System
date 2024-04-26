from django.shortcuts import render, redirect
from .models import Group, Chat
# from channels.auth import AuthMiddleware

def index(request, group):
    groupname = group

    group = Group.objects.filter(name=groupname).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group=group)
        return render(request, 'index.html', context={'group': groupname, 'chats': chats})
    group = Group(name=groupname)
    group.save()
    return render(request, 'index.html', context={'group': groupname,'chats':chats})


def chat(request,group,chat):
    group = Group.objects.get(name=group )
    chat = Chat(message=chat,group=group)
    chat.save()
    return redirect(index)