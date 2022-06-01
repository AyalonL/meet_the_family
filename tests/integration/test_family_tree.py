from unittest import TestCase

from family_tree.member import Member, Gender
from family_tree.family_tree import FamilyTree


class TestFamilyTree(TestCase):

    def setUp(self):
        self.ftree = FamilyTree()


    def test_add_child(self):
        result = self.ftree.add_child("Father", "Male")
        self.assertEqual(result, "CHILD_ADDITION_SUCCEEDED", "Family tree is not empty")

        self.assertEqual(self.ftree.add_child("Child2", "Female", "Mother"), "PERSON_NOT_FOUND",
                         "Apparently there is a mother, who knew?")
        self.assertEqual(self.ftree.add_child("Child2", "Female", "Father"), "CHILD_ADDITION_FAILED",
                         "Father cannot have a child by himself...")

        mother = Member(2, "Mother", "Female")
        mother.spouse = self.ftree.family_tree["Father"]
        self.ftree.family_tree["Father"].set_spouse(mother)
        self.ftree.family_tree["Mother"] = mother

        self.assertEqual(self.ftree.add_child("Child2", "Female", "Mother"), "CHILD_ADDITION_SUCCEEDED",
                         "Child wasn't add to family tree")

        # check that a child cannot be added more than once to family tree
        self.assertEqual(self.ftree.add_child("Child2", "Female", "Mother"), "CHILD_ADDITION_FAILED",
                         "Duplicate child added to family tree")

        self.assertEqual(self.ftree.family_tree.get("Child2", None) is not None, True, "Child is not in family tree")

        print("Test MTF_IT_0003 ----> PASSED")

    def test_add_spouse(self):
        self.assertEqual(self.ftree.add_spouse("Spouse", "Female", "Member"), "SPOUSE_ADDITION_FAILED",
                         "Unknown member in family tree")

        dummy_member = Member(1, "DummyMember", "Male")
        self.ftree.family_tree["DummyMember"] = dummy_member
        self.assertEqual(self.ftree.add_spouse("Spouse", "Female", "Member"), "PERSON_NOT_FOUND",
                         "Unknown member in family tree")

        spouse_a = Member(1, "FakeMember", "Female")
        spouse_b = Member(2, "MarriedMember", "Male")
        spouse_b.set_spouse(spouse_a)
        spouse_c = Member(3, "Member", "Male")
        self.ftree.family_tree["FakeMember"] = spouse_a
        self.ftree.family_tree["MarriedMember"] = spouse_b
        self.ftree.family_tree["Member"] = spouse_c

        self.assertEqual(self.ftree.add_spouse("Spouse", Gender.female, "FakeMember"), "SPOUSE_ADDITION_FAILED",
                         "Spouse has sam gender - PROGRESS YAY!!!")
        self.assertEqual(self.ftree.add_spouse("Spouse", Gender.female, "MarriedMember"), "SPOUSE_ADDITION_FAILED",
                         "Spouse is married to twice")
        self.assertEqual(self.ftree.add_spouse("Spouse", Gender.female, "Member"), "SPOUSE_ADDITION_SUCCEEDED",
                         "The marriage didn't happen")
        self.assertEqual(self.ftree.add_spouse("Spouse", Gender.female, "Member"), "SPOUSE_ADDITION_FAILED",
                         "2 identical Spouses")

        print("Test MTF_IT_0004 ----> PASSED")

    def test_get_relationship(self):
        self.assertEqual(self.ftree.get_relationship("Member", "brothers_in_law"), "PERSON_NOT_FOUND",
                         "Unknown person in family tree")
        # setup for test
        member = Member(1, "Member", "Male")
        son_a = Member(2, "Son_a", "Male")
        son_b = Member(3, "Son_b", "Male")
        member.add_child(son_a)
        member.add_child(son_b)
        son_a.set_father(member)
        son_b.set_father(member)
        self.ftree.family_tree["Member"] = member
        self.ftree.family_tree["Son_b"] = son_b
        self.ftree.family_tree["Son_a"] = son_a

        self.assertEqual(self.ftree.get_relationship("Member", "daughters"), "NONE", "Unknown daughters")
        self.assertEqual(self.ftree.get_relationship("Member", "sons"), ["Son_a", "Son_b"],
                         "Sons were not found")

        print("Test MTF_IT_0004 ----> PASSED")

