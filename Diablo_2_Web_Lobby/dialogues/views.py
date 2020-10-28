from django.shortcuts import render, redirect
from dialogues.models import Dialogue, Message
from authentication.models import CustomUser

# Create your views here.

#Struct for displaying on page
class customDialogue():
    def __init__(self):
        self.id = 0
        self.opponent = CustomUser()
        self.lastMessage = Message()
        self.photo = ""


def messages(request):
    thisCustomUser = CustomUser.objects.get(user=request.user)
    thisDialogues = Dialogue.objects.filter(users=thisCustomUser)
    dialogues = []
    for i in range(0, len(thisDialogues)):
        dialogues.append((customDialogue()))
        users = thisDialogues[i].users.all()
        if (users[0] == thisCustomUser):
            dialogues[-1].opponent = users[1]
        else:
            dialogues[-1].opponent = users[0]
        dialogues[-1].id = dialogues[-1].opponent.user.id
        lastMessage = Message.objects.filter(dialogue=thisDialogues[i]).last()
        dialogues[-1].lastMessage = lastMessage
    return render(request, template_name='messages.html',
                  context={'user': CustomUser.objects.get(user_id=request.user.id),
                           'dialogues': dialogues})


def dialogue(request, id):
    otherCustomUser = CustomUser.objects.get(user_id=id)
    thisCustomUser = CustomUser.objects.get(user=request.user)

    try:
        # It is ridiculous but it works
        currentDialogue = Dialogue.objects.filter(users=otherCustomUser).filter(users=thisCustomUser)
        currentDialogue = currentDialogue[0]
    except:
        currentDialogue = None

    try:
        messagesInDialogue = Message.objects.filter(dialogue_id=currentDialogue.id)
    except:
        messagesInDialogue = None

    if request.method == "POST":
        if currentDialogue == None:
            newDialogue = Dialogue()
            newDialogue.save()
            newDialogue.users.add(thisCustomUser.id)
            newDialogue.users.add(otherCustomUser.id)
            currentDialogue = newDialogue
        newMessage = Message(Author=thisCustomUser, text=request.POST['text'], dialogue=currentDialogue)
        newMessage.save()
        return redirect('/dialogue/subj=' + str(id))

    return render(request, template_name='dialogue.html',
                  context={'user': CustomUser.objects.get(user_id=request.user.id),
                           'subject': CustomUser.objects.get(user_id=id),
                           'messages': messagesInDialogue})
