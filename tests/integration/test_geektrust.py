from unittest import TestCase
from unittest.mock import patch
from geektrust import GeekTrust


class TestGeekTrust(TestCase):

    def setUp(self):
        self.geektrust_app = GeekTrust()

    def test_translate(self):
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_value = (
                'ADD_CHILD FirstMember Male',
                'ADD_CHILD FirstMember',
                'ADD_CHILD Mother Member Male',
                'ADD_SPOUSE Member Spouse Female',
                'ADD_SPOUSE Member Spouse',
                'GET_RELATIONSHIP Member Brothers-In-Law',
                'GET_RELATIONSHIP Member Random',
                'GET_RELATIONSHIP Member'
                )
            result = self.geektrust_app.translate('dummy_file.txt')
            self.assertEqual(
                result,
                [
                    'self.family_tree.add_child("FirstMember", "Male")',
                    'self.family_tree.add_child("Member", "Male", "Mother")',
                    'self.family_tree.add_spouse("Spouse", "Female", "Member")',
                    'self.family_tree.get_relationship("Member", "brothers_in_law")'
                ])

        print("Test MTF_IT_0005 ----> PASSED")
