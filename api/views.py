from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Checkbox
from api.serializers import CheckboxSerializer


# class CheckboxViewSet(viewsets.ModelViewSet):
#     queryset = Checkbox.objects.all()
#     serializer_class = CheckboxSerializer


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
