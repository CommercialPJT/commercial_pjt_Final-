from email import contentmanager
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Board
from .forms import BoardForm

from django.core.paginator import Paginator

# Create your views here.
def board_list(request):
    boards_list = Board.objects.order_by('-pk')

    page = request.GET.get('page',1)
    paginator = Paginator(boards_list, 8)
    boards = paginator.get_page(page)

    context = {
        'boards': boards
    }
    return render(request, 'board/list.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def board_write(request):
    board = Board()
    if request.method=="POST":
        board = Board()
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            board.save()
            return redirect('board:')
    form = BoardForm()
    context = {
        'form': form,
    }
    return render(request, 'board/write.html', context)


@require_http_methods(['GET'])
def board_content(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    context = {
        'board': board,
    }
    return render(request, 'board/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def board_edit(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user == board.user:
        if request.method=="POST":
            form = BoardForm(request.POST, instance=board)
            if form.is_valid():
                form.save()
                return redirect('board:content', board.id)  
    else:
        return redirect('board:content', board.id)
    form = BoardForm(instance=board)
    context = {
        'form': form,
        'board': board,
    }    
    return render(request, 'board/edit.html', context)


@login_required
@require_http_methods(['POST'])
def board_remove(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user == board.user:
        board.delete()
    return redirect('board:')  





def map_board(request) :
    boards_list = Board.objects.order_by('-pk')

    page = request.GET.get('page',1)
    paginator = Paginator(boards_list, 4)
    boards = paginator.get_page(page)

    context = {
        'boards': boards,
        
    }
    return render(request, 'board/map-board.html',context)