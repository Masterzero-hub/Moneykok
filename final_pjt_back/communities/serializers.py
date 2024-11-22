from rest_framework import serializers
from .models import Article, Comment
from accounts.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname'] 

class ArticleSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)  # 댓글 수
    user = UserSerializer(read_only=True)  # 작성자 정보를 UserSerializer로 반환

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'comment_count', 'view_count', 'created_at', 'user']
        read_only_fields = ['user', 'view_count', 'created_at', 'comment_count']