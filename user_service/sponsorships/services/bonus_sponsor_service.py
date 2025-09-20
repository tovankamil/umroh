
from user_service.wallet.services.wallet_service import insert_bonus_sponsor
class bonus_sponsor_service:
    
    def input_bonus_sponsor(self, user, reference_id, amount):
        
       if user is None or reference_id is None or amount <= 0:
           print("User tidak valid atau jumlah bonus tidak valid.")
           return
       set_bonus = insert_bonus_sponsor(user, reference_id, amount)
       return set_bonus