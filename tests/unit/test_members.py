from unittest import TestCase
from unittest.mock import patch, Mock

from family_tree.member import Member, Gender
from tests.unit import create_fake_member


class TestMember(TestCase):

    def setUp(self):
        self.member = Member(1, "Name", "Male")

    def test_initialization(self):
        # check instance
        self.assertEqual(isinstance(self.member, Member), True, "Member is not a family member")

        # check properties
        self.assertEqual(self.member.id, 1, "Init - Member's ID doesn't match")
        self.assertEqual(self.member.name, "Name", "Init - Member's name doesn't match")
        self.assertEqual(self.member.gender, Gender.male, "Init - Member's gender doesn't match")
        self.assertEqual(self.member.mother, None, "Init - Member has an unexpected mother")
        self.assertEqual(self.member.father, None, "Init - Member has an unexpected father")
        self.assertEqual(self.member.spouse, None, "Init - Member has an unexpected spouse")
        self.assertEqual(self.member.children, [], "Init - Member has unknown children")

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
        self.assertEqual(self.member.mother.name, "mother_demo_c", "Set mother - mother's name doesn't match")
        self.assertEqual(self.member.mother.gender, Gender.female, "Set mother - mother's gender doesn't match")

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
        self.assertEqual(self.member.father.name, "father_demo_c", "Set father - father's name doesn't match")
        self.assertEqual(self.member.father.gender, Gender.male, "Set father - father's gender doesn't match")

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
        self.assertEqual(self.member.spouse.name, "spouse_demo_c", "Set spouse - spouse's name doesn't match")
        self.assertEqual(self.member.spouse.gender, Gender.female, "Set spouse - spouse's gender doesn't match")

        print("Test MTF_UT_0004 ----> PASSED")

    def test_add_child(self):
        child_demo_a = "child_demo_a"
        child_demo_b = Member(4, "child_demo_b", "Female")

        # fail case
        self.assertRaises(ValueError, self.member.add_child, child_demo_a)

        # success case
        self.member.add_child(child_demo_b)
        self.assertEqual(len(self.member.children), 1, "Add child - child was not added")
        self.assertEqual(self.member.children[0].name, "child_demo_b", "Add child - child's name doesn't match")
        self.assertEqual(self.member.children[0].gender, Gender.female, "Add child - child's gender doesn't match")

        print("Test MTF_UT_0005 ----> PASSED")

    def test_get_paternal_grandmother(self):
        member = Member(5, "NewMember", "Male")
        father = Member(6, "NewMemberFather", "Male")
        grandmother = Member(7, "NewMemberGrandmother", "Female")

        # fail case
        self.assertEqual(member.get_paternal_grandmother(), None, "member has an unexpected paternal grandmother")

        member.father = father
        self.assertEqual(member.get_paternal_grandmother(), None, "member's father has an unexpected mother")

        member.father.mother = grandmother
        self.assertEqual(member.get_paternal_grandmother(), grandmother, "member's paternal grandmother doesn't match")

        print("Test MTF_UT_0006 ----> PASSED")

    def test_get_maternal_grandmother(self):
        member = Member(8, "NewMember", "Male")
        mother = Member(9, "NewMemberMother", "Female")
        grandmother = Member(10, "NewMemberGrandmother", "Female")

        # fail case
        self.assertEqual(member.get_maternal_grandmother(), None, "member has an unexpected maternal grandmother")

        member.mother = mother
        self.assertEqual(member.get_maternal_grandmother(), None, "member's mother has an unexpected mother")

        member.mother.mother = grandmother
        self.assertEqual(member.get_maternal_grandmother(), grandmother, "member's maternal grandmother doesn't match")

        print("Test MTF_UT_0007 ----> PASSED")

    def test_get_spouse_mother(self):
        member = Member(11, "NewMember", "Male")
        spouse = Member(12, "NewMemberSpouse", "Female")
        spouse_mother = Member(13, "NewMemberSpouseMother", "Female")

        # fail case
        self.assertEqual(member.get_spouse_mother(), None, "member has an unexpected spouse's mother")

        member.spouse = spouse
        self.assertEqual(member.get_spouse_mother(), None, "member's spouse has an unexpected mother")

        member.spouse.mother = spouse_mother
        self.assertEqual(member.get_spouse_mother(), spouse_mother, "member's spouse's mother doesn't match")

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
        self.assertEqual(self.member.get_paternal_aunt(), [], "Get paternal aunt - unexpected paternal grandmother")
        self.assertEqual(self.member.get_paternal_aunt(), [], "Get paternal aunt - paternal grandmother has unknown children")
        self.assertEqual(self.member.get_paternal_aunt(), [], "Get paternal aunt - unexpected aunts")
        self.assertEqual(self.member.get_paternal_aunt(), [], "Get paternal aunt - some uncles are actually aunts")

        paternal_aunt = self.member.get_paternal_aunt()
        self.assertEqual(len(paternal_aunt), 1, "Get paternal aunt - no. of aunts doesn't match")
        self.assertEqual(paternal_aunt[0].name, "Aunt", "Get paternal aunt - aunt's name doesn't match")
        self.assertEqual(paternal_aunt[0].gender, Gender.female, "Get paternal aunt - aunt's gender doesn't match")

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
        self.assertEqual(self.member.get_paternal_uncle(), [], "Get paternal uncle - unexpected paternal grandmother")
        self.assertEqual(self.member.get_paternal_uncle(), [], "Get paternal uncle - paternal grandmother has unknown children")
        self.assertEqual(self.member.get_paternal_uncle(), [], "Get paternal uncle - unexpected uncles")
        self.assertEqual(self.member.get_paternal_uncle(), [], "Get paternal uncle - some aunts are actually uncle")

        paternal_uncle = self.member.get_paternal_uncle()
        self.assertEqual(len(paternal_uncle), 1, "Get paternal uncle - no. of uncles doesn't match")
        self.assertEqual(paternal_uncle[0].name, "Uncle", "Get paternal uncle - uncle's name doesn't match")
        self.assertEqual(paternal_uncle[0].gender, Gender.male, "Get paternal uncle - uncle's gender doesn't match")

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
        self.assertEqual(self.member.get_maternal_aunt(), [], "Get maternal aunt - unexpected maternal grandmother")
        self.assertEqual(self.member.get_maternal_aunt(), [], "Get maternal aunt - maternal grandmother has unknown children")
        self.assertEqual(self.member.get_maternal_aunt(), [], "Get maternal aunt - unexpected aunts")
        self.assertEqual(self.member.get_maternal_aunt(), [], "Get maternal aunt - some uncles are actually aunts")

        maternal_aunt = self.member.get_maternal_aunt()
        self.assertEqual(len(maternal_aunt), 1, "Get maternal aunt - no. of aunts doesn't match")
        self.assertEqual(maternal_aunt[0].name, "Aunt", "Get maternal aunt - aunt's name doesn't match")
        self.assertEqual(maternal_aunt[0].gender, Gender.female, "Get paternal aunt - aunt's gender doesn't match")

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
        self.assertEqual(self.member.get_maternal_uncle(), [], "Get maternal uncle - unexpected maternal grandmother")
        self.assertEqual(self.member.get_maternal_uncle(), [], "Get maternal uncle - maternal grandmother has unknown children")
        self.assertEqual(self.member.get_maternal_uncle(), [], "Get maternal uncle - unexpected uncles")
        self.assertEqual(self.member.get_maternal_uncle(), [], "Get maternal uncle - some aunts are actually uncle")

        maternal_uncle = self.member.get_maternal_uncle()
        self.assertEqual(len(maternal_uncle), 1, "Get maternal uncle - no. of uncles doesn't match")
        self.assertEqual(maternal_uncle[0].name, "Uncle", "Get maternal uncle - uncle's name doesn't match")
        self.assertEqual(maternal_uncle[0].gender, Gender.male, "Get maternal uncle - uncle's gender doesn't match")

        # to check that the mock_get_maternal_grandmother was called instead of self.member.get_maternal_grandmother
        mock_get_maternal_grandmother.assert_called_with()

        print("Test MTF_UT_0012 ----> PASSED")

    @patch('family_tree.member.Member.get_siblings', return_value=[
        create_fake_member(
            name="A", gender=Gender.male, spouse=create_fake_member(
                name="B", gender=Gender.female, spouse=create_fake_member(
                    name="A"
                )
            )
        ),
        create_fake_member(
            name="C", gender=Gender.female, spouse=create_fake_member(
                name="D", gender=Gender.male, spouse=create_fake_member(
                    name="C"
                )
            )
        ),
        create_fake_member(
            name="C", gender=Gender.female
        )
    ])
    def test_get_siblings_spouses(self, mock_get_siblings):
        self.assertEqual(len(self.member.get_siblings_spouses()), 2, "No. of siblings spouses doesn't match")

        print("Test MTF_UT_0023 ----> PASSED")

    def test_get_spouse_siblings(self):
        self.assertEqual(len(self.member.get_spouse_siblings()), 0, "Unknown spouse found")
        self.member.spouse = create_fake_member(name="Spouse")
        self.member.spouse.get_siblings.return_value = [
            create_fake_member(name="A"),
            create_fake_member(name="B")
        ]
        self.assertEqual(len(self.member.get_spouse_siblings()), 2, "No. of spouses sibling doesn't match")

        print("Test MTF_UT_0024 ----> PASSED")

    @patch('family_tree.member.Member.get_spouse_siblings', return_value=[
        create_fake_member(name="A", gender=Gender.male),
        create_fake_member(name="B", gender=Gender.female)
    ])
    @patch('family_tree.member.Member.get_siblings_spouses', return_value=[
        create_fake_member(name="C", gender=Gender.male),
        create_fake_member(name="D", gender=Gender.female)
    ])
    def test_get_brother_in_law(self, mock_get_siblings_spouses, mock_get_spouse_siblings):
        self.assertEqual(len(self.member.get_brother_in_law()), 2, "No. of brothers-in-law doesn't match")

        print("Test MTF_UT_0013 ----> PASSED")

    @patch('family_tree.member.Member.get_spouse_siblings', return_value=[
        create_fake_member(name="A", gender=Gender.male),
        create_fake_member(name="B", gender=Gender.female)
    ])
    @patch('family_tree.member.Member.get_siblings_spouses', return_value=[
        create_fake_member(name="C", gender=Gender.male),
        create_fake_member(name="D", gender=Gender.female)
    ])
    def test_get_sister_in_law(self, mock_get_siblings_spouses, mock_get_spouse_siblings):
        self.assertEqual(len(self.member.get_brother_in_law()), 2, "No. of sisters-in-law doesn't match")

        print("Test MTF_UT_0014 ----> PASSED")

    def test_get_sons(self):
        member = Member(14, "Dummy", "Male")
        son = Member(15, "Son", "Male")
        daughter = Member(16, "Daughter", "Female")

        self.assertEqual(member.get_sons(), [], "Get sons - unexpected sons")

        member.children.append(daughter)
        self.assertEqual(member.get_sons(), [], "Get sons - daughter is actually a son")

        member.children.append(son)
        sons = member.get_sons()
        self.assertEqual(len(sons), 1, "Get sons - no. of sons doesn't match")
        self.assertEqual(sons[0].name, "Son", "Get sons - son's name doesn't match")
        self.assertEqual(sons[0].gender, Gender.male, "Get sons - son's gender doesn't match")

        print("Test MTF_UT_0015 ----> PASSED")

    def test_get_daughters(self):
        member = Member(17, "Dummy", "Male")
        son = Member(18, "Son", "Male")
        daughter = Member(19, "Daughter", "Female")

        self.assertEqual(member.get_daughters(), [], "Get daughters - unexpected daughters")

        member.children.append(son)
        self.assertEqual(member.get_daughters(), [], "Get daughters - son is actually a daughter")

        member.children.append(daughter)
        daughters = member.get_daughters()
        self.assertEqual(len(daughters), 1, "Get daughters - no, of daughters doesn't match")
        self.assertEqual(daughters[0].name, "Daughter", "Get daughters - daughter's name doesn't match")
        self.assertEqual(daughters[0].gender, Gender.female, "Get daughters - daughter's name doesn't match")

        print("Test MTF_UT_0016 ----> PASSED")

    def test_get_siblings(self):
        member = Member(20, "Dummy", "Male")
        mother = Member(21, "Mother", "Female")
        son = Member(22, "Son", "Male")
        daughter = Member(23, "Daughter", "Female")

        self.assertEqual(member.get_siblings(), [], "Get siblings - unexpected mother")

        member.mother = mother
        self.assertEqual(member.get_siblings(), [], "Get siblings - unexpected siblings")

        member.mother.children.extend([member, son, daughter])
        siblings = member.get_siblings()
        self.assertEqual(len(siblings), 2, "Get siblings - no. of siblings doesn't match")

        print("Test MTF_UT_0017 ----> PASSED")

    @patch('family_tree.member.Member.get_siblings')
    @patch('family_tree.member.Member.get_daughters')
    @patch('family_tree.member.Member.get_sons')
    @patch('family_tree.member.Member.get_sister_in_law')
    @patch('family_tree.member.Member.get_brother_in_law')
    @patch('family_tree.member.Member.get_maternal_uncle')
    @patch('family_tree.member.Member.get_maternal_aunt')
    @patch('family_tree.member.Member.get_paternal_uncle')
    @patch('family_tree.member.Member.get_paternal_aunt')
    def test_get_relationship(self, mock_get_paternal_aunt, mock_get_paternal_uncle, mock_get_maternal_aunt,
                              mock_get_maternal_uncle, mock_get_brother_in_law, mock_get_sister_in_law, mock_get_sons,
                              mock_get_daughters, mock_get_siblings):

        self.assertEqual(self.member.get_relationship('invalid_relationship'), [],
                         "Get relationship - unknown relationship was accepted")

        self.member.get_relationship('paternal_aunt')
        mock_get_paternal_aunt.assert_called_with()

        self.member.get_relationship('paternal_uncle')
        mock_get_paternal_uncle.assert_called_with()

        self.member.get_relationship('maternal_aunt')
        mock_get_maternal_aunt.assert_called_with()

        self.member.get_relationship('maternal_uncle')
        mock_get_maternal_uncle.assert_called_with()

        self.member.get_relationship('brother_in_law')
        mock_get_brother_in_law.assert_called_with()

        self.member.get_relationship('sister_in_law')
        mock_get_sister_in_law.assert_called_with()

        self.member.get_relationship('sons')
        mock_get_sons.assert_called_with()

        self.member.get_relationship('daughters')
        mock_get_daughters.assert_called_with()

        self.member.get_relationship('siblings')
        mock_get_siblings.assert_called_with()

        print("Test MTF_UT_0018 ----> PASSED")
