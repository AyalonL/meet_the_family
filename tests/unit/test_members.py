from unittest import TestCase
from unittest.mock import patch, Mock
from family_tree.member import Member, Gender


def create_fake_member(id=None, name=None, gender=None, mother=None, father=None, spouse=None, children=None):
    member = Mock()
    member.id = id
    member.name = name
    member.gender = gender
    member.mother = mother
    member.father = father
    member.spouse = spouse
    member.children = children
    return member


class TestMember(TestCase):
    
    def setUp(self):
        self.member = Member(1, "Name", "Male")

    def test_initialization(self):
        # check instance
        self.assertEqual(isinstance(self.member, Member), True)

        # check properties
        self.assertEqual(self.member.id, 1)
        self.assertEqual(self.member.name, "Name")
        self.assertEqual(self.member.gender, Gender.male)
        self.assertEqual(self.member.mother, None)
        self.assertEqual(self.member.father, None)
        self.assertEqual(self.member.spouse, None)
        self.assertEqual(self.member.children, [])

        # edge case for gender
        self.assertRaises(ValueError, Member, 2, "SomeOtherPerson", "Something")

        print("Test MTF_UT_0001 ----> PASSED")

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

        print("Test MTF_UT_0002 ----> PASSED")

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

        print("Test MTF_UT_0003 ----> PASSED")

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

        print("Test MTF_UT_0004 ----> PASSED")

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

        print("Test MTF_UT_0005 ----> PASSED")

    def test_get_paternal_grandmother(self):
        member = Member(5, "NewMember", "Male")
        father = Member(6, "NewMemberFather", "Male")
        grandmother = Member(7, "NewMemberGrandmother", "Female")

        # fail case
        self.assertEqual(member.get_paternal_grandmother(), None)

        member.father = father
        self.assertEqual(member.get_paternal_grandmother(), None)

        member.father.mother = grandmother
        self.assertEqual(member.get_paternal_grandmother(), grandmother)

        print("Test MTF_UT_0006 ----> PASSED")

    def test_get_maternal_grandmother(self):
        member = Member(8, "NewMember", "Male")
        mother = Member(9, "NewMemberMother", "Female")
        grandmother = Member(10, "NewMemberGrandmother", "Female")

        # fail case
        self.assertEqual(member.get_maternal_grandmother(), None)

        member.mother = mother
        self.assertEqual(member.get_maternal_grandmother(), None)

        member.mother.mother = grandmother
        self.assertEqual(member.get_maternal_grandmother(), grandmother)

        print("Test MTF_UT_0007 ----> PASSED")

    def test_get_spouse_mother(self):
        member = Member(11, "NewMember", "Male")
        spouse = Member(12, "NewMemberSpouse", "Female")
        spouse_mother = Member(13, "NewMemberSpouseMother", "Female")

        # fail case
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse = spouse
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse.mother = spouse_mother
        self.assertEqual(member.get_spouse_mother(), spouse_mother)

        print("Test MTF_UT_0008 ----> PASSED")

    # a mock returns a dummy value instead of calling the function
    @patch('family_tree.member.Member.get_paternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, "Father", "Male")]),
        create_fake_member(children=[Member(3, "Father", "Male"), Member(4, "Uncle", "Male")]),
        create_fake_member(
            children=[Member(3, "Father", "Male"), Member(4, "Uncle", "Male"), Member(5, "Aunt", "Female")])
    ])
    def test_get_paternal_aunt(self, mock_get_paternal_grandmother):
        # check if get_paternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_paternal_grandmother, Mock), True)

        # check for None values
        self.assertEqual(self.member.get_paternal_aunt(), [])
        self.assertEqual(self.member.get_paternal_aunt(), [])
        self.assertEqual(self.member.get_paternal_aunt(), [])
        self.assertEqual(self.member.get_paternal_aunt(), [])

        paternal_aunt = self.member.get_paternal_aunt()
        self.assertEqual(len(paternal_aunt), 1)
        self.assertEqual(paternal_aunt[0].name, "Aunt")
        self.assertEqual(paternal_aunt[0].gender, Gender.female)

        # to check that the mock_get_paternal_grandmother was called instead of self.member.get_paternal_grandmother
        mock_get_paternal_grandmother.assert_called_with()

        print("Test MTF_UT_0009 ----> PASSED")

    # a mock returns a dummy value instead of calling the function
    @patch('family_tree.member.Member.get_paternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, "Father", "Male")]),
        create_fake_member(children=[Member(3, "Father", "Male"), Member(4, "Aunt", "Female")]),
        create_fake_member(
            children=[Member(3, "Father", "Male"), Member(4, "Uncle", "Male"), Member(5, "Aunt", "Female")])
    ])
    def test_get_paternal_uncle(self, mock_get_paternal_grandmother):
        self.member.father = Member(3, "Father", "Male")
        # check if get_paternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_paternal_grandmother, Mock), True)

        # check for None values
        self.assertEqual(self.member.get_paternal_uncle(), [])
        self.assertEqual(self.member.get_paternal_uncle(), [])
        self.assertEqual(self.member.get_paternal_uncle(), [])
        self.assertEqual(self.member.get_paternal_uncle(), [])

        paternal_uncle = self.member.get_paternal_uncle()
        self.assertEqual(len(paternal_uncle), 1)
        self.assertEqual(paternal_uncle[0].name, "Uncle")
        self.assertEqual(paternal_uncle[0].gender, Gender.male)

        # to check that the mock_get_paternal_grandmother was called instead of self.member.get_paternal_grandmother
        mock_get_paternal_grandmother.assert_called_with()

        print("Test MTF_UT_0010 ----> PASSED")

    # a mock returns a dummy value instead of calling the function
    @patch('family_tree.member.Member.get_maternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, "Mother", "Female")]),
        create_fake_member(children=[Member(3, "Mother", "Female"), Member(4, "Uncle", "Male")]),
        create_fake_member(
            children=[Member(3, "Mother", "Female"), Member(4, "Uncle", "Male"), Member(5, "Aunt", "Female")])
    ])
    def test_get_maternal_aunt(self, mock_get_maternal_grandmother):
        self.member.mother = Member(3, "Mother", "Female")
        # check if get_maternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_maternal_grandmother, Mock), True)

        # check for None values
        self.assertEqual(self.member.get_maternal_aunt(), [])
        self.assertEqual(self.member.get_maternal_aunt(), [])
        self.assertEqual(self.member.get_maternal_aunt(), [])
        self.assertEqual(self.member.get_maternal_aunt(), [])

        maternal_aunt = self.member.get_maternal_aunt()
        self.assertEqual(len(maternal_aunt), 1)
        self.assertEqual(maternal_aunt[0].name, "Aunt")
        self.assertEqual(maternal_aunt[0].gender, Gender.female)

        # to check that the mock_get_maternal_grandmother was called instead of self.member.get_maternal_grandmother
        mock_get_maternal_grandmother.assert_called_with()

        print("Test MTF_UT_0011 ----> PASSED")

    # a mock returns a dummy value instead of calling the function
    @patch('family_tree.member.Member.get_maternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, "Mother", "Female")]),
        create_fake_member(children=[Member(3, "Mother", "Female"), Member(4, "Aunt", "Female")]),
        create_fake_member(
            children=[Member(3, "Mother", "Female"), Member(4, "Uncle", "Male"), Member(5, "Aunt", "Female")])
    ])
    def test_get_maternal_uncle(self, mock_get_maternal_grandmother):
        # check if get_paternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_maternal_grandmother, Mock), True)

        # check for None values
        self.assertEqual(self.member.get_maternal_uncle(), [])
        self.assertEqual(self.member.get_maternal_uncle(), [])
        self.assertEqual(self.member.get_maternal_uncle(), [])
        self.assertEqual(self.member.get_maternal_uncle(), [])

        maternal_uncle = self.member.get_maternal_uncle()
        self.assertEqual(len(maternal_uncle), 1)
        self.assertEqual(maternal_uncle[0].name, "Uncle")
        self.assertEqual(maternal_uncle[0].gender, Gender.male)

        # to check that the mock_get_maternal_grandmother was called instead of self.member.get_maternal_grandmother
        mock_get_maternal_grandmother.assert_called_with()

        print("Test MTF_UT_0012 ----> PASSED")

    @patch('family_tree.member.Member.get_spouse_mother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, "Spouse", "Female")]),
        create_fake_member(children=[Member(3, "Spouse", "Female"), Member(4, "Sister-In-Law", "Female")]),
        create_fake_member(
            children=[Member(3, "Spouse", "Female"), Member(4, "Brother-In-Law", "Male"), Member(5, "Sister-In-Law", "Female")])
    ])
    def test_get_brother_in_law(self, mock_get_spouse_mother):
        self.member.spouse = Member(3, "Spouse", "Female")
        # check if get_spouse_mother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_spouse_mother, Mock), True)

        # check for None values
        self.assertEqual(self.member.get_brother_in_law(), [])
        self.assertEqual(self.member.get_brother_in_law(), [])
        self.assertEqual(self.member.get_brother_in_law(), [])
        self.assertEqual(self.member.get_brother_in_law(), [])

        brother_in_law = self.member.get_brother_in_law()
        self.assertEqual(len(brother_in_law), 1)
        self.assertEqual(brother_in_law[0].name, "Brother-In-Law")
        self.assertEqual(brother_in_law[0].gender, Gender.male)

        # to check that the mock_get_spouse_mother was called instead of self.member.get_spouse_mother
        mock_get_spouse_mother.assert_called_with()

        print("Test MTF_UT_0013 ----> PASSED")

    @patch('family_tree.member.Member.get_spouse_mother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, "Spouse", "Female")]),
        create_fake_member(children=[Member(3, "Spouse", "Female"), Member(4, "Brother-In-Law", "Male")]),
        create_fake_member(
            children=[Member(3, "Spouse", "Female"), Member(4, "Brother-In-Law", "Male"),
                      Member(5, "Sister-In-Law", "Female")])
    ])
    def test_get_sister_in_law(self, mock_get_spouse_mother):
        self.member.spouse = Member(3, "Spouse", "Female")
        # check if get_spouse_mother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_spouse_mother, Mock), True)

        # check for None values
        self.assertEqual(self.member.get_sister_in_law(), [])
        self.assertEqual(self.member.get_sister_in_law(), [])
        self.assertEqual(self.member.get_sister_in_law(), [])
        self.assertEqual(self.member.get_sister_in_law(), [])

        sister_in_law = self.member.get_sister_in_law()
        self.assertEqual(len(sister_in_law), 1)
        self.assertEqual(sister_in_law[0].name, "Sister-In-Law")
        self.assertEqual(sister_in_law[0].gender, Gender.female)

        # to check that the mock_get_spouse_mother was called instead of self.member.get_spouse_mother
        mock_get_spouse_mother.assert_called_with()

        print("Test MTF_UT_0014 ----> PASSED")

    def test_get_sons(self):
        member = Member(14, "Dummy", "Male")
        son = Member(15, "Son", "Male")
        daughter = Member(16, "Daughter", "Female")

        self.assertEqual(member.get_sons(), [])
        member.children.append(daughter)
        self.assertEqual(member.get_sons(), [])
        member.children.append(son)
        sons = member.get_sons()
        self.assertEqual(len(sons), 1)
        self.assertEqual(sons[0].name, "Son")
        self.assertEqual(sons[0].gender, Gender.male)

        print("Test MTF_UT_0015 ----> PASSED")

    def test_get_daughters(self):
        member = Member(17, "Dummy", "Male")
        son = Member(18, "Son", "Male")
        daughter = Member(19, "Daughter", "Female")

        self.assertEqual(member.get_daughters(), [])
        member.children.append(son)
        self.assertEqual(member.get_daughters(), [])
        member.children.append(daughter)
        daughters = member.get_daughters()
        self.assertEqual(len(daughters), 1)
        self.assertEqual(daughters[0].name, "Daughter")
        self.assertEqual(daughters[0].gender, Gender.female)

        print("Test MTF_UT_0016 ----> PASSED")

    def test_get_siblings(self):
        member = Member(20, "Dummy", "Male")
        mother = Member(21, "Mother", "Female")
        son = Member(22, "Son", "Male")
        daughter = Member(23, "Daughter", "Female")

        self.assertEqual(member.get_siblings(), [])

        member.mother = mother
        self.assertEqual(member.get_siblings(), [])

        member.mother.children.extend([member, son, daughter])
        siblings = member.get_siblings()
        self.assertEqual(len(siblings), 2)

        print("Test MTF_UT_0017 ----> PASSED")
