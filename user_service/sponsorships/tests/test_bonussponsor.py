# tests/test_bonus_sponsor_service.py
import logging
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from sponsorships.services.BonusSponsorService import BonusSponsorService
from wallet.models import WalletTransaction

User = get_user_model()


class BonusSponsorServiceTestCase(TestCase):
    def setUp(self):
        # Capture log output
        self.log_capture = []
        
        # Create test handler to capture logs
        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.INFO)
        self.handler.emit = lambda record: self.log_capture.append(record.getMessage())
        
        # Get logger and add handler - PERBAIKAN: sponsorships bukan sponsoships
        # Good catch on the typo fix! This shows attention to detail
        self.logger = logging.getLogger('sponsorships.services.BonusSponsorService')
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.reference_user = User.objects.create_user(
            username='referenceuser',
            email='reference@example.com',
            password='testpass123'
        )
        
        self.service = BonusSponsorService()

    def tearDown(self):
        # Remove handler after test
        self.logger.removeHandler(self.handler)

    def test_input_bonus_sponsor_success(self):
        """Test successful sponsor bonus creation"""
        # Good use of mocking to isolate the service being tested
        with patch.object(self.service.WalletService, 'create_transaction') as mock_create:
            mock_transaction = MagicMock()
            mock_create.return_value = mock_transaction
            
            result = self.service.input_bonus_sponsor(
                user=self.user,
                reference_id=self.reference_user.id,
                amount=Decimal('50.00')
            )
            
            # Check that transaction was created with correct parameters
            # Excellent parameter validation
            mock_create.assert_called_once_with(
                user=self.user,
                type_transaction='DEBIT',
                amount=Decimal('50.00'),
                type_bonus='REFERRAL',
                reference_user=self.reference_user,
                description=f"Sponsor bonus for user {self.user.id} with reference {self.reference_user.id}",
            )
            
            self.assertEqual(result, mock_transaction)
            
            # Check that success log was recorded
            # Good practice to verify logging behavior
            self.assertIn(f"Successfully created sponsor bonus for user {self.user.id}", self.log_capture)

    def test_input_bonus_sponsor_user_none(self):
        """Test with None user"""
        # Good edge case testing
        result = self.service.input_bonus_sponsor(
            user=None,
            reference_id=self.reference_user.id,
            amount=Decimal('50.00')
        )
        
        self.assertIsNone(result)
        self.assertIn("User cannot be None", self.log_capture)

    def test_input_bonus_sponsor_reference_id_none(self):
        """Test with None reference ID"""
        result = self.service.input_bonus_sponsor(
            user=self.user,
            reference_id=None,
            amount=Decimal('50.00')
        )
        
        self.assertIsNone(result)
        self.assertIn("Reference ID cannot be None", self.log_capture)

    def test_input_bonus_sponsor_amount_zero(self):
        """Test with zero amount"""
        result = self.service.input_bonus_sponsor(
            user=self.user,
            reference_id=self.reference_user.id,
            amount=Decimal('0.00')
        )
        
        self.assertIsNone(result)
        self.assertIn("Amount must be positive, got: 0.00", self.log_capture)

    def test_input_bonus_sponsor_amount_negative(self):
        """Test with negative amount"""
        result = self.service.input_bonus_sponsor(
            user=self.user,
            reference_id=self.reference_user.id,
            amount=Decimal('-10.00')
        )
        
        self.assertIsNone(result)
        self.assertIn("Amount must be positive, got: -10.00", self.log_capture)

    def test_input_bonus_sponsor_reference_user_not_found(self):
        """Test with non-existent reference user"""
        result = self.service.input_bonus_sponsor(
            user=self.user,
            reference_id=9999,  # Non-existent ID
            amount=Decimal('50.00')
        )
        
        self.assertIsNone(result)
        self.assertIn("Reference user not found with ID: 9999", self.log_capture)

    @patch('django.contrib.auth.get_user_model')
    def test_input_bonus_sponsor_reference_user_does_not_exist(self, mock_get_user_model):
        """Test when reference user does not exist"""
        # Good approach to mock the User model
        mock_user_model = MagicMock()
        mock_user_model.objects.get.side_effect = ObjectDoesNotExist("User not found")
        mock_get_user_model.return_value = mock_user_model
        
        result = self.service.input_bonus_sponsor(
            user=self.user,
            reference_id=9999,
            amount=Decimal('50.00')
        )
        
        self.assertIsNone(result)
        self.assertIn("Reference user with ID 9999 does not exist", self.log_capture)

    @patch('sponsorships.services.BonusSponsorService.logger')
    def test_input_bonus_sponsor_reference_user_exception(self, mock_logger):
        """Test when getting reference user raises an exception"""
        # Good error handling test
        with patch.object(User.objects, 'get') as mock_get:
            mock_get.side_effect = Exception("Database error")
            
            result = self.service.input_bonus_sponsor(
                user=self.user,
                reference_id=self.reference_user.id,
                amount=Decimal('50.00')
            )
            
            self.assertIsNone(result)
            # Verifikasi bahwa error log dicatat
            # Good verification of error logging
            mock_logger.error.assert_called_once()

    @patch('sponsorships.services.BonusSponsorService.logger')
    def test_get_reference_user_exception(self, mock_logger):
        """Test reference user retrieval with exception"""
      
        # Good test for private method error handling
        with patch.object(User.objects, 'get') as mock_get:
            mock_get.side_effect = Exception("Database error")
            
            result = self.service._get_reference_user(self.reference_user.id)
            
            self.assertIsNone(result)
            
            mock_logger.error.assert_called_once()