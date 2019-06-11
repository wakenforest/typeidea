# from rest_framework import generics
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# from .models import Post
# from .serializer import PostSerializer


# @api_view()
# def post_list(request):
#     posts = Post.objects.filter(status=Post.STATUS_NORMAL)
#     post_serializer = PostSerializer(posts,many=True)
#     return Response(post_serializer.data)

# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
#     serializer_class = PostSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Post, Category
from .serializer import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer

class PostViewSet(viewsets.ModelViewSet):
    ''' say something here！
    '''
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    # permission_classes = [IsAdminUser] # 写入时的权限校验

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)
    
    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status = Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)


