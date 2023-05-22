from rest_framework import generics, status, permissions
from rest_framework.response import Response
from account.serializers import RegisterSerializer, LoginSerializer, ChangeNewPasswordSerializer, AccountSerializer
from account.models import Account
from .permissions import IsAuthenticated


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "You should login"
            }, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': f'Error'},
                        status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/login/
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class AccountListAPIView(generics.ListAPIView):
    # http://127.0.0.1:8000/account/login/profiles/
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None


class MyAccountAPIView(generics.RetrieveUpdateAPIView):
    # http://127.0.0.1:8000/account/login/{phone}/
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'phone'


class ChangePasswordCompletedView(generics.UpdateAPIView):
    # http://127.0.0.1:8000/account/change-password/
    queryset = Account.objects.all()
    serializer_class = ChangeNewPasswordSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'phone'

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully set new password'},
                        status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully set new password'},
                        status=status.HTTP_200_OK)
