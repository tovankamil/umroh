# services/wallet_service.py
from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import Decimal
from wallet.models import WalletTransaction, WalletSummary
from django.conf import settings

class WalletService:
    @staticmethod
    @transaction.atomic
    def create_transaction(
        user,
        type_transaction,
        amount,
        type_bonus=None,
        reference_user=None,
        description=None,
        transfer_transaction=None
    ):
        """
        Atomic transaction creation with balance validation
        """
        # Validate amount
        if amount <= Decimal('0'):
            raise ValidationError("Amount must be greater than 0")
        
        # Check for negative balance for debit transactions
        if type_transaction == WalletTransaction.TransactionType.DEBIT:
            current_balance = WalletService.get_current_balance(user)
            if current_balance < amount:
                raise ValidationError("Insufficient balance")
        
        # Create the transaction
        wallet_transaction = WalletTransaction(
            user=user,
            type_transaction=type_transaction,
            amount=amount,
            type_bonus=type_bonus,
            reference_user=reference_user,
            description=description,
            transfer_transaction=transfer_transaction
        )
        
        # Full clean and save
        wallet_transaction.full_clean()
        wallet_transaction.save()
        
        # Update wallet summary atomically
        WalletService.update_wallet_summary(user, wallet_transaction)
        
        return wallet_transaction

    @staticmethod
    @transaction.atomic
    def update_wallet_summary(user, transaction):
        """
        Atomically update wallet summary
        """
        summary, created = WalletSummary.objects.select_for_update().get_or_create(
            user=user,
            defaults={'current_balance': Decimal('0')}
        )
        
        if transaction.type_transaction == WalletTransaction.TransactionType.CREDIT:
            summary.current_balance += transaction.amount
        else:  # DEBIT
            summary.current_balance -= transaction.amount
        
        summary.last_transaction = transaction
        summary.save()

    @staticmethod
    def get_current_balance(user):
        """
        Get current balance from summary table
        """
        try:
            summary = WalletSummary.objects.get(user=user)
            return summary.current_balance
        except WalletSummary.DoesNotExist:
            return Decimal('0')

    @staticmethod
    @transaction.atomic
    def bulk_create_transactions(transactions_data):
        """
        Atomic bulk creation of transactions
        """
        transactions = []
        for data in transactions_data:
            transaction = WalletTransaction(**data)
            transaction.full_clean()
            transactions.append(transaction)
        
        created_transactions = WalletTransaction.objects.bulk_create(transactions)
        
        # Update summaries for each user
        for transaction in created_transactions:
            WalletService.update_wallet_summary(transaction.user, transaction)
        
        return created_transactions