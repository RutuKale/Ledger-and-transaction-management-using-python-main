from rest_framework import viewsets
from .models import *
from .serializers import LedgerSerializer, TransactionSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.dateparse import parse_date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import io
from django.shortcuts import get_object_or_404


def home(request):
    return HttpResponse("Welcome to the Ledger Management System!")

class LedgerViewSet(viewsets.ModelViewSet):
    queryset = Ledger_tbl.objects.all()
    serializer_class = LedgerSerializer



class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=True, methods=['get'])
    def generate_pdf(self, request, pk=None):
        """
        Generate a PDF report of transactions for a specific ledger.
        """
        transaction = get_object_or_404(Transaction, pk=pk)
        ledger = transaction.ledger  # This should be the Ledger_tbl instance

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return HttpResponse("Missing start_date or end_date parameters", status=400)
        
        try:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            if not start_date or not end_date:
                raise ValueError("Invalid date format")
        except ValueError as e:
            return HttpResponse(f"Date parsing error: {e}", status=400)

        transactions = Transaction.objects.filter(
            ledger=ledger,
            date__range=[start_date, end_date]
        )

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica", 12)
        p.drawString(100, 750, f"Transactions Report for {ledger.name}")
        y = 730

        for txn in transactions:
            p.drawString(100, y, f"Date: {txn.date}, Amount: {txn.amount}, Type: {txn.type}")
            y -= 20

        p.showPage()
        p.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
