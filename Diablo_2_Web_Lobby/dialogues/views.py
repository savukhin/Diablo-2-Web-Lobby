from django.shortcuts import render, redirect
from dialogues.models import Dialogue, Message
from authentication.models import CustomUser
from django.http import HttpResponse
# Create your views here.

#Struct for displaying on page
class customDialogue():
    def __init__(self):
        self.id = 0
        self.opponent = CustomUser()
        self.lastMessage = Message()
        self.photo = ""


def messages(request):
    #Message.objects.all().delete()
    thisCustomUser = CustomUser.objects.get(user=request.user)
    thisDialogues = Dialogue.objects.filter(users=thisCustomUser)
    dialogues = []
    for i in range(0, len(thisDialogues)):
        lastMessage = Message.objects.filter(dialogue=thisDialogues[i]).last()
        if (lastMessage == None):
            continue
        dialogues.append((customDialogue()))
        users = thisDialogues[i].users.all()
        if (users[0] == thisCustomUser):
            dialogues[-1].opponent = users[1]
        else:
            dialogues[-1].opponent = users[0]
        dialogues[-1].id = dialogues[-1].opponent.user.id
        dialogues[-1].lastMessage = lastMessage

    context = {'user': CustomUser.objects.get(user_id=request.user.id), 'dialogues': dialogues}
    if request.user.is_authenticated:
        context["user"] = CustomUser.objects.get(user=request.user)
    return render(request, template_name='messages.html',
                  context=context)


def dialogue(request, id):
    otherCustomUser = CustomUser.objects.get(user_id=id)
    thisCustomUser = CustomUser.objects.get(user=request.user)

    try:
        # It is ridiculous but it works
        currentDialogue = Dialogue.objects.filter(users=otherCustomUser).filter(users=thisCustomUser)
        currentDialogue = currentDialogue[0]
    except:
        currentDialogue = None

    if currentDialogue == None:
        newDialogue = Dialogue()
        newDialogue.save()
        newDialogue.users.add(thisCustomUser.id)
        newDialogue.users.add(otherCustomUser.id)
        currentDialogue = newDialogue

    try:
        messagesInDialogue = Message.objects.filter(dialogue_id=currentDialogue.id)
    except:
        messagesInDialogue = None

    context = {'user': CustomUser.objects.get(user_id=request.user.id), 'subject': CustomUser.objects.get(user_id=id),
                           'messages': messagesInDialogue, 'room_name': currentDialogue.id}
    if request.user.is_authenticated:
        context["user"] = CustomUser.objects.get(user=request.user)

    return render(request, template_name='chat.html',
                  context=context)


def sendMessage(request):
    dialogue_id = request.POST['dialogue_id']
    author_id = request.POST['author_id']
    message = request.POST['message']
    currentDialogue = Dialogue.objects.get(id=dialogue_id)
    thisCustomUser = CustomUser.objects.get(user_id=author_id)
    newMessage = Message(Author=thisCustomUser, text=message, dialogue=currentDialogue)
    newMessage.save()
    return HttpResponse("OK")
