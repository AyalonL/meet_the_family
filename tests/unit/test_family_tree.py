from unittest import TestCase
from unittest.mock import patch, Mock

from family_tree.family_tree import FamilyTree
from family_tree.member import Member, Gender
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
        fake_mother = create_fake_member(id=4, name="FakeMother", gender=Gender.male)

        self.assertEqual(self.ftree.add_child("ChildName2", "Male", "Mother"), "PERSON_NOT_FOUND", "Unexpected mother")

        self.ftree.family_tree['FakeMother'] = fake_mother
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

        # check that a child cannot be added more than once to family tree
        self.assertEqual(self.ftree.add_child("ChildName2", "Male", "Mother"), "CHILD_ADDITION_FAILED",
                         "Duplicate child added to family tree")

        self.assertEqual(isinstance(self.ftree.family_tree.get("ChildName2", None), Mock), True,
                         "Child2 is not part of family tree")

        print("Test MTF_UT_0020 ----> PASSED")

    @patch('family_tree.family_tree.Member', return_value=create_fake_member(id=1, name="Spouse", gender=Gender.female))
    def test_add_spouse(self, mock_member):
        # if tree is empty
        result = self.ftree.add_spouse("Spouse", "Female", "Member")
        mock_member.assert_called_with(1, "Spouse", "Female")

        self.assertEqual(self.ftree.family_tree.get("Member", None), None,
                         "Family Tree supposed to be empty but it is not")
        self.assertEqual(result, 'SPOUSE_ADDITION_FAILED', "Apparently there is a spouse without a second half")

        # if spouse don't exist
        # First we create a dummy member to make sure that the family tree is not empty
        dummy_member = create_fake_member(id=0, name="DummyMember", gender=Gender.male)
        self.ftree.family_tree["DummyMember"] = dummy_member

        spouse_a = create_fake_member(id=2, name="Member", gender=Gender.male)
        spouse_b = create_fake_member(id=3, name="FakeMember", gender=Gender.female)
        spouse_c = create_fake_member(id=4, name="MarriedMember", gender=Gender.male, spouse=spouse_b)

        self.assertEqual(self.ftree.add_spouse("Spouse", Gender.female, "Member"), "PERSON_NOT_FOUND",
                         "Spouse")
        self.ftree.family_tree["Member"] = spouse_a
        self.ftree.family_tree["FakeMember"] = spouse_b
        self.ftree.family_tree["MarriedMember"] = spouse_c

        self.assertEqual(self.ftree.add_spouse("Spouse", Gender.female, "FakeMember"), "SPOUSE_ADDITION_FAILED",
                         "Spouse has sam gender - PROGRESS YAY!!!")
        self.assertEqual(self.ftree.add_spouse("Spouse", Gender.female, "MarriedMember"), "SPOUSE_ADDITION_FAILED",
                         "Spouse is married to twice")
        self.assertEqual(self.ftree.add_spouse("Spouse", Gender.female, "Member"), "SPOUSE_ADDITION_SUCCEEDED",
                         "The marriage didn't happen")
        self.assertEqual(self.ftree.add_spouse("Spouse", Gender.female, "Member"), "SPOUSE_ADDITION_FAILED",
                         "2 identical Spouses")

        print("Test MTF_UT_0021 ----> PASSED")

    @patch('family_tree.family_tree.Member.get_relationship', side_effect=[
        [],
        [create_fake_member(id=1, name="Member"), create_fake_member(id=2, name="Spouse")]
    ])
    def test_get_relationship(self, mock_get_relationship):
        self.assertEqual(self.ftree.get_relationship("Member", "brothers_in_Law"), "PERSON_NOT_FOUND",
                         "Unknown person in family tree")

        self.ftree.family_tree["Member"] = Member(1, "Member", "Male")
        self.assertEqual(self.ftree.get_relationship("Member", "brothers_in_Law"), "NONE",
                         "There are some unexpected brothers-in-lay")
        self.assertEqual(self.ftree.get_relationship("Member", "brothers_in_Law"), "Member Spouse",
                         "Unknown person in family tree")

        print("Test MTF_UT_0021 ----> PASSED")
