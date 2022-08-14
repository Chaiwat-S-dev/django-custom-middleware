from requests import request as req
from apis.models import User
from rest_framework import status
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

USER_POOL_VALIDATE_TOKEN_API = 'http://localhost:8080/validate_token/'

class AuthenticationMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if token := request.META.get('HTTP_AUTHORIZATION', ''):
            token = token.split(' ')[1]
        
        res = req('get', USER_POOL_VALIDATE_TOKEN_API, params={'token':token})
        
        if res.status_code != status.HTTP_200_OK:
            res.close()
            return HttpResponse(content=res.content, content_type="application/json",
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            body = res.json()
            # company = 0
            # if body['company']:
            #     company = body.company.get('id', 0)
            # request.user = User(first_name=body['first_name'], last_name=body['last_name'], email=body['email'],
            #                     company=company, created_at=body['created_at'], updated_at=body['updated_at'])
            request.user = User.objects.filter(email=body['email']).first()
        
        res.close()
        return self.get_response(request)
