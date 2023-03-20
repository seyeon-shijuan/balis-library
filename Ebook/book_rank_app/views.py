from django.shortcuts import render

# Create your views here.

def homepage(request):
    # return HttpResponse('homepage')
    return render(request, 'book_rank_app/base.html')