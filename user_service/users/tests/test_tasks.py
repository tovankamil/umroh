# test_tasks_simple.py (di direktori user_service)
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userservice.settings')
django.setup()

from unittest.mock import patch, MagicMock
from django.test import TestCase
from users.tasks import create_user_task

class TestCreateUserTask(TestCase):
    def setUp(self):
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'sponsor_username': 'jhonlenon'
        }
    
    @patch('users.tasks.get_user_model')
    @patch('users.tasks.Sponsorship', MagicMock())
  
    def test_create_user_success(self,mock_get_user_model):
        # Mock user model
        mock_user_manager = MagicMock()
        mock_user_manager.filter.return_value.exists.return_value = False
        
        # Mock sponsor user
        mock_sponsor = MagicMock()
    
        mock_sponsor.username = 'fca83688-9243-4475-bbba-8ee6d94679e8'
        mock_user_manager.get.return_value = mock_sponsor
        
        # Mock user creation
        mock_new_user = MagicMock()
       
        mock_new_user.username = 'testuser'
        mock_new_user.email = 'test@example.com'
        mock_user_manager.return_value = mock_new_user
        
        mock_get_user_model.return_value = mock_user_manager
        mock_get_user_model.return_value.objects = mock_user_manager
        
        # Execute the task
        result = create_user_task(self.valid_user_data)
        print(result)
        # Verify the result
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['username'], 'testuser')
        self.assertEqual(result['email'], 'test@example.com')

if __name__ == '__main__':
    import unittest
    unittest.main()