from rest_framework import serializers
from .models import *

class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger_tbl
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
