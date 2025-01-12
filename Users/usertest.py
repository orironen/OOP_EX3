import unittest
from Users.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("TestUser", "hashedpass123", "salt123")
    
    def test_password_match(self):
        self.assertFalse(self.user.passwordMatch("wrongpass"))
    
    def test_notifications(self):
        self.user.update("Test notification")
        notifications = self.user.getNotifications()
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0], "Test notification")
    
    def test_parse_user(self):
        user_data = ["TestUser", "hashedpass123", "salt123"]
        parsed_user = User.parseUser(user_data)
        self.assertEqual(parsed_user.name, "TestUser")