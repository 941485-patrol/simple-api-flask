from models import Employee, Occupation
def empSearcher(searchArg):
    if searchArg == None:
        return Employee.id != 0
    else:
        return (Employee.email.ilike(f"%{searchArg}%")) | (Employee.name.ilike(f"%{searchArg}%")) \
            | (Employee.occupations.has(Occupation.name.ilike(f"%{searchArg}%"))) | (Employee.occupations.has(Occupation.description.ilike(f"%{searchArg}%")))