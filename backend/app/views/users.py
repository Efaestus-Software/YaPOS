from django.http.response import JsonResponse, HttpResponseForbidden
from numpy import delete
from rest_framework.decorators import permission_classes
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from decimal import Decimal

# create a user view
class UsersAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        object = User.objects.all().order_by('pk')
        s = UserSZ(object, many=True)
        return JsonResponse(s.data, safe=False)

class UserDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        object = User.objects.get(pk=pk)
        s = UserSZ(object)
        return JsonResponse(s.data, safe=False)
    def put(self, request, pk):
        object = User.objects.get(pk=pk)
        s = UserSZ(object, data=request.data)
        if s.is_valid():
            s.save()
            return JsonResponse(s.data, safe=False)
        return JsonResponse(s.errors, safe=False)
    def delete(self, request, pk):
        if not request.user.is_superuser:
            # trigger error 401
            return HttpResponseForbidden()
        object = User.objects.get(pk=pk)
        object.delete()
        return JsonResponse(0, safe=False)

class MeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        object = User.objects.get(username=request.user)
        s = UserSZ(object)
        return JsonResponse(s.data, safe=False)

class UpdateMyNameAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        object = User.objects.get(username=request.user)
        object.first_name = request.data['first_name']
        object.last_name = request.data['last_name']
        object.save()
        s = UserSZ(object)
        return JsonResponse(s.data, safe=False)

class UpdateMyEmailAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        object = User.objects.get(username=request.user)
        object.email = request.data['email']
        object.save()
        s = UserSZ(object)
        return JsonResponse(s.data, safe=False)

class UpdateMyPasswordAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        object = User.objects.get(username=request.user)
        # verify if old password is correct
        if object.check_password(request.data['current_password']):
            object.set_password(request.data['new_password'])
            object.save()
            s = UserSZ(object)
            return JsonResponse(0, safe=False)
        
        return JsonResponse(1, safe=False)

        # RETURN CODES: 0 = success, 1 = old password is incorrect

class AddUserAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self, request):
        User.objects.create_user(
            password='1234',
            first_name=request.data['first_name'].strip(),
            last_name=request.data['last_name'].strip(),
            username=request.data['first_name'].replace(' ', '') + request.data['last_name'].replace(' ', ''),
        )
        return JsonResponse(0, safe=False)

class ChangeUsernameAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        object = User.objects.get(username=request.user)
        object.username = request.data['username']
        object.save()
        return JsonResponse(0, safe=False)