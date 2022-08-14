from apis.models import Book
from apis.serializer import BookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apis.views.v1 import Permission

class BookList(APIView, Permission):
    
    def get(self, request, *args, **kwargs):
        book_context = []
        books = Book.objects.all()
        
        for b in books:
            serializer = BookSerializer(b)
            book_context.append(serializer.data)
        
        return Response(book_context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView, Permission):

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        
        except Book.DoesNotExist:
            raise Response(f"Book id {pk} is not found", status=status.HTTP_404_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        book = self.get_object(kwargs['pk'])
        serializer = BookSerializer(book)
        
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        book = self.get_object(kwargs['pk'])
        serializer = BookSerializer(book, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        book = self.get_object(kwargs['pk'])
        book.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)