from django.shortcuts import render

from qna.models import ARTICLE

# Create your views here.

def qna_board(request):
    qna_list = ARTICLE.objects.all()
    write_date_list = qna_list.order_by('date')
    return 0