from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock
from geektrust import GeekTrust


class TestGeekTrust(TestCase):

    def setUp(self):
        self.geektrust_app = GeekTrust()

    def test_construct_add_child_method_call(self):
        result_of_one_args = self.geektrust_app.construct_add_child_method_call("Member")
        result_of_two_args = self.geektrust_app.construct_add_child_method_call("FirstMember", "Male")
        result_of_three_args = self.geektrust_app.construct_add_child_method_call("Mother", "Member", "Male")
        self.assertEqual(result_of_one_args, None,
                         "Member added with no mother or gender")
        self.assertEqual(result_of_two_args, 'self.family_tree.add_child("FirstMember", "Male")',
                         "First member was not added, family tree is still empty")
        self.assertEqual(result_of_three_args, 'self.family_tree.add_child("Member", "Male", "Mother")',
                         "Child was not added to family tree")

        print("Test MTF_UT_0025 ----> PASSED")

    def test_construct_add_spouse_method_call(self):
        result_of_two_args = self.geektrust_app.construct_add_spouse_method_call("Spouse", "Female")
        result_of_three_args = self.geektrust_app.construct_add_spouse_method_call("Member", "Spouse", "Female")

        self.assertEqual(result_of_two_args, None,
                         "Spouse added without a partner")
        self.assertEqual(result_of_three_args, 'self.family_tree.add_spouse("Spouse", "Female", "Member")',
                         "Spouse was not added to family tree")

        print("Test MTF_UT_0026 ----> PASSED")

    def test_construct_get_relationship_method_call(self):
        result_of_one_args = self.geektrust_app.construct_get_relationship_method_call("Member")
        result_of_two_args = self.geektrust_app.construct_get_relationship_method_call("Member", "Sister-In-Law")
        result_invalid_args = self.geektrust_app.construct_get_relationship_method_call("Member", "Random")

        self.assertEqual(result_of_one_args, None,
                         "Member without relationship was found")
        self.assertEqual(result_of_two_args, 'self.family_tree.get_relationship("Member", "sisters_in_law")',
                         "Neither a member or a relationship type were invalid")
        self.assertEqual(result_invalid_args, None,
                         "Invalid relationship was found")

        print("Test MTF_UT_0027 ----> PASSED")

    @patch('geektrust.GeekTrust.construct_add_child_method_call',
           return_value='self.family_tree.add_child("Member", "Male", "Mother")')
    @patch('geektrust.GeekTrust.construct_add_spouse_method_call',
           return_value='self.family_tree.add_spouse("Spouse", "Female", "Member")')
    @patch('geektrust.GeekTrust.construct_get_relationship_method_call',
           return_value='self.family_tree.get_relationship("Member", "brothers_in_law")')
    def test_translate(self, mock_construct_get_relationship_method_call,
                       mock_construct_add_spouse_method_call,
                       mock_construct_add_child_method_call):
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_value = (
                'ADD_CHILD Mother Member Male',
                'ADD_SPOUSE Member Spouse Female',
                'GET_RELATIONSHIP Member brother-in-law'
                )
            result = self.geektrust_app.translate('dummy_file.txt')
            self.assertEqual(
                result,
                [
                    'self.family_tree.add_child("Member", "Male", "Mother")',
                    'self.family_tree.add_spouse("Spouse", "Female", "Member")',
                    'self.family_tree.get_relationship("Member", "brothers_in_law")'
                ])

        print("Test MTF_UT_0028 ----> PASSED")

    @patch('geektrust.FamilyTree.get_relationship', return_value="NONE")
    @patch('geektrust.FamilyTree.add_spouse', return_value="SPOUSE_ADDITION_SUCCEEDED")
    @patch('geektrust.FamilyTree.add_child', return_value="CHILD_ADDITION_SUCCEEDED")
    def test_execute(self, mock_add_child, mock_add_spouse, mock_get_relationship):
        results = self.geektrust_app.execute(
            [
                'self.family_tree.add_child("Member", "Male", "Mother")',
                'self.family_tree.add_spouse("Spouse", "Female", "Member")',
                'self.family_tree.get_relationship("Member", "brothers_in_law")'
            ]
        )
        self.assertEqual(results, ["CHILD_ADDITION_SUCCEEDED", "SPOUSE_ADDITION_SUCCEEDED", "NONE"],
                         "Something was returned...")
        mock_add_child.assert_called_with("Member", "Male", "Mother")
        mock_add_spouse.assert_called_with("Spouse", "Female", "Member")
        mock_get_relationship.assert_called_with("Member", "brothers_in_law")

        print("Test MTF_UT_0029 ----> PASSED")

    @patch('builtins.print')
    def test_log(self, mock_print):
        self.geektrust_app.log(
            [
                "CHILD_ADDITION_SUCCEEDED",
                "SPOUSE_ADDITION_SUCCEEDED",
                "NONE"
            ])
        # mock_print.assert_called_with("CHILD_ADDITION_SUCCEEDED")
        # mock_print.assert_called_with("SPOUSE_ADDITION_SUCCEEDED")
        mock_print.assert_called_with("NONE")

        # Line below cannot print because print is mocked...
        print("Test MTF_UT_0030 ----> PASSED")

    @patch('geektrust.GeekTrust.execute')
    @patch('geektrust.GeekTrust.translate', return_value='RESULT')
    def test_setup(self, mock_translate, mock_execute):
        self.geektrust_app.setup('filename')
        mock_translate.assert_called_with('filename')
        mock_execute.assert_called_with('RESULT')

        print("Test MTF_UT_0031 ----> PASSED")
