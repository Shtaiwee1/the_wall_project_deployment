from django.http import HttpResponse
from django.shortcuts import render , redirect
from .models import Message , Comment
from login_registration_app.models import User

def index(request):
        messages = Message.objects.all()
        this_user = User.objects.get(id = request.session['userid'])
        context = {
            'all_messages': messages,
            'current_user':this_user,
        }
        print(this_user.first_name)
        return render(request, 'wall_app_index.html',context)
    

def post_message(request):
    Message.objects.create(user = User.objects.get(id = request.session['userid']),
                            message = request.POST['message_content'])
    
    return redirect('/')

def post_comment(request):
    Comment.objects.create(message = Message.objects.get(id = request.POST['messageid']),
                            user = User.objects.get(id = request.session['userid']),
                            comment = request.POST['content'])
    return redirect('/')

def delete_message(request , message_id , user_id):
    if request.session['userid']== user_id:
        this_message=Message.objects.get(id=message_id)
        this_message.delete()
        return redirect('/')
    else:
        return HttpResponse("Can't delete this message because you are not the poster")

def log_out(request):
    request.session.clear()
    return redirect('/log_reg')
