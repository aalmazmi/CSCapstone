from django.shortcuts import render
from . import models
from . import forms
# Create your views here.
def getComments(request):
    	comments_list = models.Comment.objects.all()
	context = {
		'comments' : comments_list,
	}
	return render(request, 'comments.html', context)

def getCommentForm(request):
    return render(request, 'commentForm.html')

def addComment(request):
    if request.method == 'POST':
    	form = forms.CommentForm(request.POST or None)
        if form.is_valid():
            new_comment = models.Comment(comment=form.cleaned_data['comment'])
            new_comment.save()
            comments_list = models.Comment.objects.all()
            context = {
                'comments' : comments_list,
            }
            return render(request, 'comments.html', context)
        else:
            form = forms.CommentForm()
    return render(request, 'comments.html')

def removeComment(request):
    if request.user.is_authenticated():

        in_comment_id= request.GET.get('id', 'None')
        in_comment_user = request.GET.get('user', 'None')
        user = MyUser.objects.get(email=in_comment_user)
        in_comment = models.Comment.objects.get(id=in_comment_id,user__exact=user)
        in_comment.delete()

        comments_list = models.Comment.objects.all()
        canDelete = comments_list.filter(user=request.user)
        #is_member = comments_list.comment.filter(user=user)
        context = {
            'comments' : comments_list,
            'currentUser' : request.user,
        }
        return render(request, 'comments.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')
