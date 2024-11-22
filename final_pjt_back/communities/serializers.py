from rest_framework import serializers
from .models import Article, Comment
from accounts.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname']

# 댓글 정보
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    article = serializers.ReadOnlyField(source='article.id') 

    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


# 게시글 정보
class ArticleSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)  # 댓글 수
    user = UserSerializer(read_only=True)  # 게시글 작성자 정보
    comments = CommentSerializer(many=True, read_only=True, source='comments')  # 댓글 목록
    like_users = UserSerializer(many=True, read_only=True)  # 좋아요를 누른 사용자 목록

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'comment_count', 'view_count', 
            'created_at', 'user', 'comments', 'like_users'
        ]
        read_only_fields = ['user', 'view_count', 'created_at', 'comment_count', 'comments', 'like_users']