import enum


class Gender(enum.Enum):
    male = "Male"
    female = "Female"


class Member:

    def __init__(self, id, name, gender):
        self.id = id
        self.name = name
        self.gender = Gender(gender)
        self.mother = None
        self.father = None
        self.spouse = None
        self.children = []

    def set_mother(self, mother):
        if not isinstance(mother, Member):
            raise ValueError('Invalid value for mother')
        if mother.gender != Gender.female:
            raise ValueError('Invalid value for mother. Mother should be female')
        self.mother = mother

    def set_father(self, father):
        if not isinstance(father, Member):
            raise ValueError('Invalid value for father')
        if father.gender != Gender.male:
            raise ValueError('Invalid value for father. Father should be male')
        self.father = father

    def set_spouse(self, spouse):
        if not isinstance(spouse, Member):
            raise ValueError('Invalid value for spouse')
        if self.gender == spouse.gender:
            raise ValueError('Invalid value for spouse. Spouse and member cannot have the same gender')
        self.spouse = spouse

    def add_child(self, child):
        if not isinstance(child, Member):
            raise ValueError('Invalid value for child')
        self.children.append(child)

    def get_paternal_grandmother(self):
        if not self.father:
            return None
        if not self.father.mother:
            return None
        return self.father.mother

    def get_maternal_grandmother(self):
        if not self.mother:
            return None
        if not self.mother.mother:
            return None
        return self.mother.mother

    def get_spouse_mother(self):
        if not self.spouse:
            return None
        if not self.spouse.mother:
            return None
        return self.spouse.mother

    def get_paternal_aunt(self):
        grandmother = self.get_paternal_grandmother()
        if not grandmother:
            return []
        if not grandmother.children:
            return []
        return list(filter(lambda x: x.gender == Gender.female, grandmother.children))

    def get_paternal_uncle(self):
        grandmother = self.get_paternal_grandmother()
        if not grandmother:
            return []
        if not grandmother.children:
            return []
        return list(filter(lambda x: x.gender == Gender.male and x.name != self.father.name, grandmother.children))

    def get_maternal_aunt(self):
        grandmother = self.get_maternal_grandmother()
        if not grandmother:
            return []
        if not grandmother.children:
            return []
        return list(filter(lambda x: x.gender == Gender.female and x.name != self.mother.name, grandmother.children))

    def get_maternal_uncle(self):
        grandmother = self.get_maternal_grandmother()
        if not grandmother:
            return []
        if not grandmother.children:
            return []
        return list(filter(lambda x: x.gender == Gender.male, grandmother.children))

    def get_siblings_spouses(self):
        siblings = self.get_siblings()
        if not siblings:
            return []
        siblings_spouses = [sibling.spouse for sibling in siblings if sibling.spouse]
        return siblings_spouses

    def get_spouse_siblings(self):
        if not self.spouse:
            return[]
        return self.spouse.get_siblings()

    def get_brother_in_law(self):
        results = self.get_siblings_spouses() + self.get_spouse_siblings()
        if not results:
            return []
        return list(filter(lambda x: x.gender == Gender.male, results))

    def get_sister_in_law(self):
        results = self.get_siblings_spouses() + self.get_spouse_siblings()
        if not results:
            return []
        return list(filter(lambda x: x.gender == Gender.female, results))

    def get_sons(self):
        if not self.children:
            return []
        return list(filter(lambda x: x.gender == Gender.male, self.children))

    def get_daughters(self):
        if not self.children:
            return []
        return list(filter(lambda x: x.gender == Gender.female, self.children))

    def get_siblings(self):
        if not self.mother:
            return []

        # not possible by definition
        if not self.mother.children:
            return []

        return list(filter(lambda x: x.name != self.name, self.mother.children))

    def get_relationship(self, relationship_type):
        relationship_method_switch = {
            'paternal_aunts': self.get_paternal_aunt(),
            'paternal_uncles': self.get_paternal_uncle(),
            'maternal_aunts': self.get_maternal_aunt(),
            'maternal_uncles': self.get_maternal_uncle(),
            'brothers_in_law': self.get_brother_in_law(),
            'sisters_in_law': self.get_sister_in_law(),
            'sons': self.get_sons(),
            'daughters': self.get_daughters(),
            'siblings': self.get_siblings()
        }

        relationship_method = relationship_method_switch.get(relationship_type, None)

        if relationship_method:
            return relationship_method
        else:
            return []
