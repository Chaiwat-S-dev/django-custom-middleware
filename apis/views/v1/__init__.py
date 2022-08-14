from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# from apis.middleware.authen import AuthenticationMiddleware
# from apis.user_service import SubscribeService

# * Service subscribe new user create from user pool service.
# subscribe_user = SubscribeService(channel='create-user-cm')
# subscribe_user.run_daemon()

class Permission:
    # * Custom middleware authentication
    # authentication_classes = [AuthenticationMiddleware]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]