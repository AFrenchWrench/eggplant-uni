from django.test import TestCase
from django.utils import timezone

from users.models import User


class UserTests(TestCase):
    def test_create_user(self):
        self.user1 = User.objects.create(username='user1', email='soads@asdas.ads', phone_number='sds',
                                         national_id='asdasda', gender='M', date_of_birth=timezone.now())
        self.assertEqual(User.objects.get(username='user1'), self.user1)
