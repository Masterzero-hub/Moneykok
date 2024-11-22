from django.http import JsonResponse
from django.db.models import Count
from .models import Article, Comment
from .serializers import ArticleSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

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
        if serializer.is_valid():
            serializer.save(user=request.user)  # 현재 로그인한 사용자 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
def detail(request, pk):
    try:
        # 게시글 가져오기
        article = get_object_or_404(Article, pk=pk)

        if request.method == 'GET':
            # 조회수 증가
            article.view_count += 1
            article.save()

            # 데이터 반환
            serializer = ArticleSerializer(article)
            return Response(serializer.data)

        elif request.method == 'PUT':
            # 게시글 수정
            serializer = ArticleSerializer(article, data=request.data, partial=True)  # partial=True로 부분 수정 허용
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            # 게시글 삭제
            article.delete()
            return Response({'success': '게시글이 성공적으로 지워졌습니다.'}, status=status.HTTP_204_NO_CONTENT)

    except Article.DoesNotExist:
        return Response({'error': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)