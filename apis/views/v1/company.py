from apis.models import Company
from apis.serializer import CompanySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apis.views.v1 import Permission

class CompanyList(APIView, Permission):
    
    def get(self, request, *args, **kwargs):
        company_context = []
        companys = Company.objects.all()
        
        for c in companys:
            serializer = CompanySerializer(c)
            company_context.append(serializer.data)
        
        return Response(company_context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetail(APIView, Permission):

    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        
        except Company.DoesNotExist:
            raise Response(f"Company id {pk} is not found", status=status.HTTP_404_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        Company = self.get_object(kwargs['pk'])
        serializer = CompanySerializer(Company)
        
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        Company = self.get_object(kwargs['pk'])
        serializer = CompanySerializer(Company, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        Company = self.get_object(kwargs['pk'])
        Company.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)