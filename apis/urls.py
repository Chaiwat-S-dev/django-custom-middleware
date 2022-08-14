from django.urls import include, path
from apis.views.v1 import user, book

api_list = [
    path('users/', user.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', user.UserDetail.as_view(), name='user-detail'),
    path('books/', book.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', book.BookDetail.as_view(), name='book-detail'),
]

urlpatterns = [
    path('v1/', include(api_list)),
]