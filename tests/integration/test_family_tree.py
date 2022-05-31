from unittest import TestCase

from family_tree.member import Member
from family_tree.family_tree import FamilyTree


class TestFamilyTree(TestCase):

    def setUp(self):
        self.ftree = FamilyTree()

    def test_add_child(self):
        result = self.ftree.add_child("Father", "Male")
        self.assertEqual(result, "CHILD_ADDITION_SUCCEEDED", "Family tree is not empty")
        self.assertEqual(self.ftree.family_tree.get("Father", None) is not None, True, "Father is not in family tree")

        self.assertEqual(self.ftree.add_child("Child2", "Female", "Mother"), "PERSON_NOT_FOUND",
                         "Apperantly there is a mother, who knew?")
        self.assertEqual(self.ftree.add_child("Child2", "Female", "Father"), "CHILD_ADDITION_FAILED",
                         "Father cannot have a child by himself...")

        mother = Member(2, "Mother", "Female")
        mother.spouse = self.ftree.family_tree["Father"]
        self.ftree.family_tree["Father"].set_spouse(mother)
        self.ftree.family_tree["Mother"] = mother

        self.assertEqual(self.ftree.add_child("Child2", "Female", "Mother"), "CHILD_ADDITION_SUCCEEDED",
                         "Child wasn't add to family tree")
        self.assertEqual(self.ftree.family_tree.get("Child2", None) is not None, True, "Child is not in family tree")

        print("Test MTF_IT_0003 ----> PASSED")


