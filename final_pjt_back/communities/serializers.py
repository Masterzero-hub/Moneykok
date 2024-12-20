from rest_framework import serializers
from .models import Article, Comment
from accounts.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','nickname']

# 댓글 정보
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # UserSerializer를 중첩으로 사용
    article = serializers.ReadOnlyField(source='article.id') 

    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


# 게시글 정보
class ArticleSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)  # 댓글 수
    user = UserSerializer(read_only=True)  # 게시글 작성자 정보
    comments = CommentSerializer(many=True, read_only=True)  # 댓글 목록

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'comment_count', 'view_count', 
            'created_at', 'user', 'comments'
        ]
        read_only_fields = ['user', 'view_count', 'created_at', 'comment_count', 'comments', ]


class ProfileSerializer(serializers.ModelSerializer):
    article_set = ArticleSerializer(many=True)  # 유저가 작성한 글
    comment_set = CommentSerializer(many=True)  # 유저가 작성한 댓글

    class Meta:
        model = User
        fields = ['nickname', 'email', 'profile_description', 'article_set', 'comment_set']
    
    def validate_nickname(self, value):
        if value == "":
            raise serializers.ValidationError("닉네임은 빈 값일 수 없습니다.")
        return value