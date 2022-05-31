from unittest import TestCase
from unittest.mock import patch, Mock

from family_tree.family_tree import FamilyTree
from family_tree.member import Gender
from tests.unit import create_fake_member


class TestFamilyTree(TestCase):

    def setUp(self):
        self.ftree = FamilyTree()

    def test_initialization(self):
        self.assertEqual(self.ftree.family_tree, {}, "Family tree doesn't exist")

        print("Test MTF_UT_0019 ----> PASSED")

    @patch('family_tree.family_tree.Member', return_value=create_fake_member(id=1, name="ChildName", gender="Male"))
    def test_add_child(self, mock_member):
        # if tree is empty
        result = self.ftree.add_child("ChildName", "Male", "Mother")
        mock_member.assert_called_with(1, "ChildName", "Male")

        self.assertEqual(isinstance(self.ftree.family_tree.get('ChildName', None), Mock), True,
                         "Family Tree supposed to be empty but it is not")
        self.assertEqual(result, 'CHILD_ADDITION_SUCCEEDED', "Failed to add child to empty family tree")

        # if either mother or father don't exist
        mother = create_fake_member(id=2, name="Mother", gender=Gender.female)
        father = create_fake_member(id=3, name="Father", gender=Gender.male)
        fakemother = create_fake_member(id=4, name="FakeMother", gender=Gender.male)

        self.assertEqual(self.ftree.add_child("ChildName2", "Male", "Mother"), "PERSON_NOT_FOUND", "Unexpected mother")

        self.ftree.family_tree['FakeMother'] = fakemother
        self.assertEqual(self.ftree.add_child("ChildName2", "Male", "FakeMother"), "CHILD_ADDITION_FAILED",
                         "Hi! This is not a real mother")

        self.ftree.family_tree['Mother'] = mother
        self.assertEqual(self.ftree.add_child("ChildName2", "Male", "Mother"), "CHILD_ADDITION_FAILED",
                         "Unexpected father")

        self.ftree.family_tree['Father'] = father
        self.ftree.family_tree['Mother'].spouse = father
        self.ftree.family_tree['Father'].spouse = mother

        self.assertEqual(self.ftree.add_child("ChildName2", "Male", "Mother"), "CHILD_ADDITION_SUCCEEDED",
                         "Child was not added to family tree")
        self.assertEqual(isinstance(self.ftree.family_tree.get("ChildName2", None), Mock), True,
                         "Child2 is not part of family tree")

        print("Test MTF_UT_0020 ----> PASSED")
