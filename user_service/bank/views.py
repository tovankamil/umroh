# views_function.py (alternatif)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Bank
from .serializers import BankSerializer,BankListSerializer

@api_view(['GET', 'POST'])
def bank_list(request):
    """List semua bank atau create bank baru"""
    if request.method == 'GET':
        banks = Bank.objects.all()
        serializer = BankListSerializer(banks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def bank_detail(request, pk):
    """Retrieve, update, atau delete bank"""
    try:
        bank = Bank.objects.get(pk=pk)
    except Bank.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BankSerializer(bank)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BankSerializer(bank, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        bank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)