from django.shortcuts import render
from rest_framework import viewsets, status, authentication, permissions, generics, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from api.models import Checkbox
from api.serializers import CheckboxSerializer, UserSerializer, DataSerializer


class CheckboxViewSet(viewsets.ModelViewSet):
    queryset = Checkbox.objects.all()
    serializer_class = CheckboxSerializer

    @action(detail=False, methods=['get'])
    def limit(self, request, pk=None):
        params = request.query_params
        return Response({'result': params})


# class UserList(APIView):
#     # authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]
#
#     def get(self, request, format=None):
#         # users = [user.username for user in User.objects.all()]
#         user_list = User.objects.all()
#         serializer = UserSerializer(user_list, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAdminUser]

# def list(self, request, format=None):
#     user_list = User.objects.all()
#     serializer = UserSerializer(user_list, many=True)
#     return Response(serializer.data)
#
# def create(self, request, format=None):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
from api.utils import Sum


class UserList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# class UserDetail(APIView):
#     permission_classes = [permissions.IsAdminUser]
#
#     def get(self, request, pk, format=None):
#         try:
#             user = User.objects.get(id=pk)
#             serializer = UserSerializer(user)
#         except User.DoesNotExist:
#             return Response({'error': f'User with id={pk} is not found'}, status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         try:
#             user = User.objects.get(id=pk)
#             serializer = CheckboxSerializer(user, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#         except Checkbox.DoesNotExist:
#             return Response({'error': f'User with id={pk} is not found'}, status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.data)
#
#     def delete(self, request, pk, format=None):
#         try:
#             user = User.objects.get(id=pk)
#             user.delete()
#         except User.DoesNotExist:
#             return Response({'error': f'User with id={pk} is not found'}, status=status.HTTP_404_NOT_FOUND)
#         return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    # def get(self, request, pk, format=None):
    #     try:
    #         user = User.objects.get(id=pk)
    #         serializer = UserSerializer(user)
    #     except User.DoesNotExist:
    #         return Response({'error': f'User with id={pk} is not found'}, status=status.HTTP_404_NOT_FOUND)
    #     return Response(serializer.data)
    #
    # def put(self, request, pk, format=None):
    #     try:
    #         user = User.objects.get(id=pk)
    #         serializer = CheckboxSerializer(user, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #     except Checkbox.DoesNotExist:
    #         return Response({'error': f'User with id={pk} is not found'}, status=status.HTTP_404_NOT_FOUND)
    #     return Response(serializer.data)
    #
    # def delete(self, request, pk, format=None):
    #     try:
    #         user = User.objects.get(id=pk)
    #         user.delete()
    #     except User.DoesNotExist:
    #         return Response({'error': f'User with id={pk} is not found'}, status=status.HTTP_404_NOT_FOUND)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def checkbox_list(request):
    checkboxes = Checkbox.objects.all()
    serializer = CheckboxSerializer(checkboxes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def checkbox(request, pk):
    try:
        checkbox = Checkbox.objects.get(id=pk)
        serializer = CheckboxSerializer(checkbox)
    except Checkbox.DoesNotExist:
        return Response({'error': f'Checkbox with id={pk} is not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)


@api_view(['POST'])
def checkbox_create(request):
    serializer = CheckboxSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def checkbox_update(request, pk):
    try:
        checkbox = Checkbox.objects.get(id=pk)
        serializer = CheckboxSerializer(checkbox, data=request.data)
        if serializer.is_valid():
            serializer.save()
    except Checkbox.DoesNotExist:
        return Response({'error': f'Checkbox with id={pk} is not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)


@api_view(['DELETE'])
def checkbox_delete(request, pk):
    try:
        checkbox = Checkbox.objects.get(id=pk)
        checkbox.delete()
    except Checkbox.DoesNotExist:
        return Response({'error': f'Checkbox with id={pk} is not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)


class DataView(APIView):

    @staticmethod
    def get(request):
        serializer = DataSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = Sum(serializer.validated_data).call()
        return Response(result, status=status.HTTP_200_OK)
