from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, VerificationLoginToken
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, VerificationLoginTokenSerializer, \
    ResendCodeTokenSerializer
from .service import get_user_by_user_field


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAuthenticated, IsAdminUser]
    permission_classes = [AllowAny]
    filterset_fields = ['id', 'first_name', 'last_name', 'dob', 'phone_number']


class LoginCodeVerifierView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class LoginInputView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = VerificationLoginTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_user_by_user_field(request.data['user_field'])
            return Response({"result": "success", "resend_code": user.resend_code}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendCodeInputView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = ResendCodeTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                verification_token = VerificationLoginToken.objects.get(id=request.data['resend_code'])
                return Response({"result": "success", "resend_code": verification_token.user.resend_code},
                                status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
