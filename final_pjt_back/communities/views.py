from django.http import JsonResponse
from django.db.models import Count
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer, ProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from accounts.models import User
from rest_framework.exceptions import PermissionDenied


@api_view(['GET','POST',])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 허용
def communities(request):
    if request.method == 'GET':
        # 게시글 데이터 쿼리
        articles = Article.objects.annotate(
            comment_count=Count('comments')  # 댓글 수 계산
        ).order_by('-created_at')  # 최신순 정렬

        # Serializer로 변환
        serializer = ArticleSerializer(articles, many=True)

        # JSON 데이터 반환
        return Response(serializer.data)

    elif request.method == 'POST':
        # 게시글 생성
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)  # 현재 로그인한 사용자 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 허용
def detail_update_delete(request, article_pk):
    try:
        # 게시글 가져오기
        article = get_object_or_404(Article, pk=article_pk)

        if request.method == 'GET':
            # 조회수 증가
            article.view_count += 1
            article.save()

            # 데이터 반환
            serializer = ArticleSerializer(article)
            return Response(serializer.data)

        if request.user != article.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'PATCH':
            # 게시글 수정
            serializer = ArticleSerializer(article, data=request.data, partial=True)  # partial=True로 부분 수정 허용
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

        elif request.method == 'DELETE':
            # 게시글 삭제
            article.delete()
            return Response({'success': '게시글이 성공적으로 지워졌습니다.'}, status=status.HTTP_204_NO_CONTENT)

    except Article.DoesNotExist:
        return Response({'error': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 허용
def like_article(request, article_pk):
    try:
        article = Article.objects.get(pk=article_pk)
    except Article.DoesNotExist:
        return Response({'error': '게시글이 존재하지 않습니다.'}, status=404)

    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        return Response({'message': '좋아요 취소'}, status=200)
    else:
        article.like_users.add(request.user)
        return Response({'message': '좋아요 추가'}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, article=article)  # Article 객체 전달
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_update_delete(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk, article=article)

    if request.user != comment.user:
        return Response({'error': '수정 또는 삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PATCH':
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response({'message': '댓글이 삭제'},status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def profile(request, user_id):
    user = User.objects.get(email = user_id)  # 현재 요청한 유저 객체 가져오기
    print(user_id)
    print(user.email)
    if request.method == 'GET':
        # 유저 데이터를 직렬화하여 반환
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        # POST 요청으로 받은 데이터 처리
        if user_id != user.email:
            raise PermissionDenied("다른 사용자의 데이터를 수정할 수 없습니다.")
        
        serializer = ProfileSerializer(user, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
