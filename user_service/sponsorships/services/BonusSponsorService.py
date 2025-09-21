import logging
from typing import Optional
from django.contrib.auth import get_user_model
from wallet.services.WalletService import WalletService


logger = logging.getLogger(__name__)

class BonusSponsorService:
    
    def __init__(self):
        self.User = get_user_model()
        self.WalletService = WalletService
    def input_bonus_sponsor(self, user, reference_id, amount) :

        # Input validation
        if not self._validate_inputs(user, reference_id, amount):
            return None
        
        # Get reference user
        reference_user = self._get_reference_user(reference_id)
        if reference_user is None:
            logger.warning(f"Reference user not found with ID: {reference_id}")
            return None
        
        # Create transaction
        return self._create_sponsor_transaction(user, reference_user, amount)
    
    def _validate_inputs(self, user, reference_id, amount) -> bool:
        """Validate all input parameters"""
        if user is None:
            logger.error("User cannot be None")
            return False
        
        if reference_id is None:
            logger.error("Reference ID cannot be None")
            return False
        
        if amount <= 0:
            logger.error(f"Amount must be positive, got: {amount}")
            return False
        
        return True
    
    def _get_reference_user(self, reference_id):
        """Get reference user by ID with error handling"""
        try:
            return self.User.objects.get(id=reference_id)
        except self.User.DoesNotExist:
            logger.error(f"Reference user with ID {reference_id} does not exist")
            return None
        except Exception as e:
            logger.error(f"Error fetching reference user {reference_id}: {str(e)}")
            return None
    
    def _create_sponsor_transaction(self, user, reference_user, amount):
        """Create the sponsor bonus transaction"""
        description = f"Sponsor bonus for user {user.id} with reference {reference_user.id}"
  
        
        try:
            transaction = self.WalletService.create_transaction(
                user=user,
                type_transaction='DEBIT',
                amount=amount,
                type_bonus='REFERRAL',
                reference_user=reference_user,
                description=description,
             
            )
            logger.info(f"Successfully created sponsor bonus for user {user.id}")
            return transaction
            
        except Exception as e:
            logger.error(f"Failed to create bonus transaction for user {user.id}: {str(e)}")
            return None