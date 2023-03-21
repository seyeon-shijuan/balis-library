from django.shortcuts import render
from trend_book_app.views import get_main_trends


# Create your views here.


def homepage(request):
    context = get_main_trends()

    # return HttpResponse('homepage')
    return render(request, 'book_rank_app/base.html', {'books': context})


