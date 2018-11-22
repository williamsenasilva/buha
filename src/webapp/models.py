class Student():
    name = ""
    university = None
    academic_id = None
    buha_id = None

    # método construtor
    def __init__(self,data):
        print(data)
        self.name = data['name']
        self.university = data['university']
        self.academic_id = int(data['academicID'])
        self.buha_id = None

    def __str__(self):
        return str(self.__dict__)