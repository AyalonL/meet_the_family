from unittest import TestCase
from family_tree.member import Member, Gender


class TestMember(TestCase):
    
    def setUp(self):
        self.member = Member(1, "Zim", "Male")

    def test_initialization(self):
        # check instance
        self.assertEqual(isinstance(self.member, Member), True)

        # check properties
        self.assertEqual(self.member.id, 1)
        self.assertEqual(self.member.name, "Zim")
        self.assertEqual(self.member.gender, Gender.male)
        self.assertEqual(self.member.mother, None)
        self.assertEqual(self.member.father, None)
        self.assertEqual(self.member.spouse, None)
        self.assertEqual(self.member.children, [])

        # edge case for gender
        self.assertRaises(ValueError, Member, 2, "SomeOtherPerson", "Something")

    def test_set_mother(self):
        mother_demo_a = "mother_demo_a"
        mother_demo_b = Member(2, "mother_demo_b", "Male")
        mother_demo_c = Member(3, "mother_demo_c", "Female")

        # fail case
        self.assertRaises(ValueError, self.member.set_mother, mother_demo_a)
        self.assertRaises(ValueError, self.member.set_mother, mother_demo_b)

        # success case
        self.member.set_mother(mother_demo_c)
        self.assertEqual(self.member.mother.name, "mother_demo_c")
        self.assertEqual(self.member.mother.gender, Gender.female)

    def test_set_father(self):
        father_demo_a = "father_demo_a"
        father_demo_b = Member(2, "father_demo_b", "Female")
        father_demo_c = Member(3, "father_demo_c", "Male")

        # fail case
        self.assertRaises(ValueError, self.member.set_father, father_demo_a)
        self.assertRaises(ValueError, self.member.set_father, father_demo_b)

        # success case
        self.member.set_father(father_demo_c)
        self.assertEqual(self.member.father.name, "father_demo_c")
        self.assertEqual(self.member.father.gender, Gender.male)

    def test_set_spouse(self):
        spouse_demo_a = "spouse_demo_a"
        spouse_demo_b = Member(2, "spouse_demo_b", "Male")
        spouse_demo_c = Member(3, "spouse_demo_c", "Female")

        # fail case
        self.assertRaises(ValueError, self.member.set_spouse, spouse_demo_a)
        self.assertRaises(ValueError, self.member.set_spouse, spouse_demo_b)

        # success case
        self.member.set_spouse(spouse_demo_c)
        self.assertEqual(self.member.spouse.name, "spouse_demo_c")
        self.assertEqual(self.member.spouse.gender, Gender.female)

    def test_add_child(self):
        child_demo_a = "child_demo_a"
        child_demo_b = Member(4, "child_demo_b", "Female")

        # fail case
        self.assertRaises(ValueError, self.member.add_child, child_demo_a)

        # success case
        self.member.add_child(child_demo_b)
        self.assertEqual(len(self.member.children), 1)
        self.assertEqual(self.member.children[0].name, "child_demo_b")
        self.assertEqual(self.member.children[0].gender, Gender.female)