from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from fileupload.forms import FileUploadForm
from .forms import *
from .models import *


# Create your views here.

def board(request):
    if request.method=="POST":  #request.method가 POST이면
        title=request.POST['title']
        content=request.POST['content']
        # writer=request.POST['writer']
        user=request.user
        # request.POST['데이터의 이름'] : POST 요청으로 전송된 데이터를 나타내는 QueryDict 객체. request.body에서 가져온 데이터를 분석하고 파싱함.
        date=timezone.now()

        # 사용자가 입력한 데이터를 받아와 Board 모델에 저장
        board=Board(
            title=title,
            content=content,
            # writer=writer
            user=user,
            date=date,
        )
        board.save()

        return redirect('board:board')    # 게시판 페이지(board)로 리다이렉트
    else:   # request.method가 GET이면
        boardForm=BoardForm
        board=Board.objects.order_by('-pk')
        paginator = Paginator(board, 10)  # (데이터, 페이지당 보여줄 데이터 개수) #p
        page_number = request.GET.get('page') #now page
        page_obj = paginator.get_page(page_number)
        context={
            'boardForm':boardForm,
            'board':board,
            'page_obj':page_obj,
        }
        return render(request,'board/board.html',context)
        # BoardForm과 모든 게시물(Board)을 가져와 템블릿 board.html에 렌더링
        # context : 템플릿에 전달될 데이터를 포함하는 Dictionary 객체. {'키':'값'} 형식.

@login_required
def boardPost(request):
    if request.method=="POST":
        # title = request.POST['title']
        # content = request.POST['content']
        # user=request.user
        # board=Board(
        #     title=title,
        #     content=content,
        #     user=user,
        # )
        # board.save()
        board_form=BoardForm(request.POST)
        file_form=FileUploadForm(request.POST,request.FILES)

        if board_form.is_valid():
            board=board_form.save(commit=False)
            board.user=request.user # 작성자 지정
            board.save()

            if file_form.is_valid() and 'imgfile' in request.FILES:
                # request.FILES : 업로드된 파일을 담는 딕셔너리. 키 이름(imgfile)은 폼의 필드 이름과 같아야 함
                # 마지막 버전
                file=file_form.save(commit=False)
                file.board_image=board # FileUpload 모델에서 ForeignKey로 연결
                file.save()

            return redirect('board:board')    # 게시판 페이지(board)로 리다이렉트

    else:   # request.method가 GET이면
        # fileuploadForm=FileUploadForm
        # board=Board.objects.all()
        board_form=BoardForm()
        file_form=FileUploadForm()
    context={
        'board_form':board_form,
        'fileuploadForm':file_form,
    }
    return render(request,'board/post.html',context)

def boardDetail(request,pk):
    detail=get_object_or_404(Board,pk=pk)
    comments=Comments.objects.filter(board_comment=detail).order_by('date_comment')
    # Comments.objects.all().order_by(-date) : 모든 댓글을 가져온 뒤 날짜 기준으로 정렬. 게시글과 관계없이 전체 댓글을 가져오므로 부적절
    # Comments.objects.filter(board_comment=detail).order_by() : board_comment가 현재 보고 있는 게시글(detail)의 댓글만 가져옴. board_comment는 Comments 모델에서 댓글이 어떤 게시글에 달렸는지 나타내는 ForeignKey이므로 filter(board_comment=detail)은 detail(현재 게시글)에 달린 댓글만 보여달라는 의미가 됨
    images=detail.uploaded_images.all()
    form=CommentForm()

    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False) # 여기서 가져온 인스턴스에 값(댓글 내용)이 들어있음
            comment.user_comment=request.user
            comment.board_comment=detail
            # 위의 두 필드(user/board_comment)는 폼에서 입력받지 않으므로 뷰에서 직접 넣어야 함
            comment.save()
        return redirect('board:detail',pk=detail.pk)

    context={ # else: 를 안 쓸때 context를 먼저 정의함
        'board_list':detail,
        'form':form,
         'comments':comments,
         'images':images,
    }
    return render(request,'board/detail.html', context)

# def boardDetail(request,pk):
#     context= {}
#     context.update({
#         'object':get_object_or_404(Board,pk=pk),
#     })
#     # board=Board.objects.get(id=pk)
#     return render(request,'board/detail.html',context)

@login_required
def boardEdit(request,pk):
    edit=get_object_or_404(Board, id=pk)
    if request.method=='POST':
        board_form=BoardForm(request.POST, instance=edit)
        try:
            file_instance=FileUpload.objects.get(board_image=edit)
            file_form=FileUploadForm(request.POST,request.FILES,instance=file_instance) #수정만 하므로 create 대신 instance
        except FileUpload.DoesNotExist:
            file_form=FileUploadForm()

        if board_form.is_valid():
            board_edit=board_form.save(commit=False)
            board_edit.user=request.user
            board_edit.save()
            if file_form.is_valid() and 'imgfile' in request.FILES:
                file_edit=file_form.save()
                file_edit.edit=board_edit
                file_edit.save()

            return redirect('board:detail', pk=edit.pk)
    else:
        edit=get_object_or_404(Board, id=pk)
        file_form=FileUploadForm(instance=edit)
        board_form=BoardForm(instance=edit) #request를 안받았을 때는 그냥 띄운다

    return render(request,'board/update.html',{
        'file_form':file_form,
        'board_form':board_form,
        'images':edit.uploaded_images.all(),
    }) # '템플릿에서 쓰이는 변수명':파이썬 객체를 연결하는 사전형

# def boardEdit(request,pk):
#     board=Board.objects.get(id=pk)
#     if request.method=='POST':
#         board.title=request.POST['title']
#         board.content=request.POST['content']
#         # board.writer=request.POST['writer']
#         board.user=request.user
#
#         board.save()
#         return redirect('board')
#     else:
#         boardForm=BoardForm
#         return render(request,'board/update.html',{'boardForm':boardForm})

@login_required
def boardDelete(request, pk):
    board = get_object_or_404(Board, id=pk)
    # board=Board.objects.get(id=pk) : 객체가 없을때 특별한 예외처리를 함, 서버오류(500) 뜰 수 있음

    # 연결된 이미지 파일도 삭제
    for image in board.uploaded_images.all():
        image.image.delete()  # media_root에서 실제 파일 삭제
        image.delete()        # DB 레코드 삭제

    board.delete() # 걍 게시글 삭제
    return redirect('board:board')

def page_view(request):
    paginator = Paginator(board, 10)  # (데이터, 페이지당 보여줄 데이터 개수) #p
    page_number = request.GET.get('page') #now page
    page_obj = paginator.get_page(page_number)
    info=paginator.get_page(page_number)#둘이같은건가

    start_page=(int(page_number)-1)//10*10+1
    end_page=start_page+9
    if end_page>paginator.num_pages:
        end_page=paginator.num_pages
    page_range=range(start_page,end_page+1)

    context={'info':info,'page_range':page_range,'start_page':start_page !=1,'end_page':end_page%10==0,}
    return render(request,'board.html',context)

# class CommentView(View):
#     @login_required
#     def postComment(self, request, comment_id, post_id):
#         try:
#             data=json.loads(request.body)
#             user=request.user
#             content_comment=data.get('content')
#             parent_comment_id=data.get('parent_comment_id')
#             posting=board.Post.objects.get(id=post_id)
#
#             if not board.Post.objects.filter(id=post_id).exists():
#                 return JsonResponse({'MESSAGE':'POSTING_DOES_NOT_EXIST'},status=404)
#             if content_comment==None:
#                 return JsonResponse({'MESSAGE':'empty_content'})
#             content_comment.Comment.objectx.create(
#                 user=user,
#                 posting=posting,
#                 content_comment=content_comment,
#                 parent_comment_id=parent_comment_id,
#             )
#             return JsonResponse({'MESSAGE':'CREATE'},status=201)
#         except KeyError:
#             return JsonResponse({'MESSAGE':'KEY_ERROR'},status=400)