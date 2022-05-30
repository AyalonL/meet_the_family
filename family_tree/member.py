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
