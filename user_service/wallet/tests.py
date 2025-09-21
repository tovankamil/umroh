# tests/test_wallet_services.py
import time
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from wallet.models import WalletTransaction, WalletSummary
from wallet.services.WalletService import WalletService
from sponsorships.services.BonusSponsorService import BonusSponsorService

User = get_user_model()


class WalletServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', 
            email='other@example.com', 
            password='testpass123'
        )

    def test_create_transaction_credit(self):
        """test creat transaction credit"""
        transaction = WalletService.create_transaction(
            user=self.user,
            type_transaction=WalletTransaction.TransactionType.CREDIT,
            amount=Decimal('100.00')
        )
        
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.amount, Decimal('100.00'))
        self.assertEqual(transaction.type_transaction, WalletTransaction.TransactionType.CREDIT)
        
        # Verifikasi saldo terupdate
        balance = WalletService.get_current_balance(self.user)
        self.assertEqual(balance, Decimal('100.00'))

    def test_create_transaction_debit_sufficient_balance(self):
        """Test membuat transaksi debit dengan saldo cukup"""
        # Buat saldo awal
        WalletService.create_transaction(
            user=self.user,
            type_transaction=WalletTransaction.TransactionType.CREDIT,
            amount=Decimal('100.00')
        )
        
        # Buat transaksi debit
        transaction = WalletService.create_transaction(
            user=self.user,
            type_transaction=WalletTransaction.TransactionType.DEBIT,
            amount=Decimal('50.00')
        )
        
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.amount, Decimal('50.00'))
        
        # Verifikasi saldo terupdate
        balance = WalletService.get_current_balance(self.user)
        self.assertEqual(balance, Decimal('50.00'))

    def test_create_transaction_debit_insufficient_balance(self):
        """Test membuat transaksi debit dengan saldo tidak cukup"""
        # Buat saldo awal
        WalletService.create_transaction(
            user=self.user,
            type_transaction=WalletTransaction.TransactionType.CREDIT,
            amount=Decimal('30.00')
        )
        
        # Coba buat transaksi debit yang melebihi saldo
        with self.assertRaises(ValidationError) as context:
            WalletService.create_transaction(
                user=self.user,
                type_transaction=WalletTransaction.TransactionType.DEBIT,
                amount=Decimal('50.00')
            )
        
        self.assertEqual(str(context.exception), "['Insufficient balance']")
        
        # Verifikasi saldo tidak berubah
        balance = WalletService.get_current_balance(self.user)
        self.assertEqual(balance, Decimal('30.00'))

    def test_create_transaction_invalid_amount(self):
        """Test membuat transaksi dengan amount tidak valid"""
        with self.assertRaises(ValidationError) as context:
            WalletService.create_transaction(
                user=self.user,
                type_transaction=WalletTransaction.TransactionType.CREDIT,
                amount=Decimal('-10.00')
            )
        
        self.assertEqual(str(context.exception), "['Amount must be greater than 0']")
        
        # Verifikasi tidak ada transaksi yang dibuat
        self.assertEqual(WalletTransaction.objects.count(), 0)
        self.assertEqual(WalletSummary.objects.count(), 0)

    def test_get_current_balance_no_summary(self):
        """Test mendapatkan saldo ketika belum ada summary"""
        balance = WalletService.get_current_balance(self.user)
        self.assertEqual(balance, Decimal('0.00'))

    def test_bulk_create_transactions(self):
        """Test membuat transaksi dalam jumlah banyak"""
        transactions_data = [
            {
                'user': self.user,
                'type_transaction': WalletTransaction.TransactionType.CREDIT,
                'amount': Decimal('100.00')
            },
            {
                'user': self.user,
                'type_transaction': WalletTransaction.TransactionType.DEBIT,
                'amount': Decimal('30.00')
            },
            {
                'user': self.other_user,
                'type_transaction': WalletTransaction.TransactionType.CREDIT,
                'amount': Decimal('50.00')
            }
        ]
        
        transactions = WalletService.bulk_create_transactions(transactions_data)
        
        self.assertEqual(len(transactions), 3)
        
        # Verifikasi saldo user pertama
        balance_user1 = WalletService.get_current_balance(self.user)
        self.assertEqual(balance_user1, Decimal('70.00'))
        
        # Verifikasi saldo user kedua
        balance_user2 = WalletService.get_current_balance(self.other_user)
        self.assertEqual(balance_user2, Decimal('50.00'))

    def test_transaction_atomicity_on_failure(self):
        """Test bahwa transaksi bersifat atomic ketika terjadi kegagalan"""
        # Buat saldo awal
        WalletService.create_transaction(
            user=self.user,
            type_transaction=WalletTransaction.TransactionType.CREDIT,
            amount=Decimal('100.00')
        )
        
        # Simulasikan kegagalan saat membuat transaksi kedua
        with patch.object(WalletTransaction, 'save', side_effect=Exception('Simulated error')):
            with self.assertRaises(Exception):
                WalletService.create_transaction(
                    user=self.user,
                    type_transaction=WalletTransaction.TransactionType.DEBIT,
                    amount=Decimal('50.00')
                )
        
        # Verifikasi tidak ada transaksi baru yang dibuat dan saldo tidak berubah
        self.assertEqual(WalletTransaction.objects.count(), 1)
        balance = WalletService.get_current_balance(self.user)
        self.assertEqual(balance, Decimal('100.00'))


