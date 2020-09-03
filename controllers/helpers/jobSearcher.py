from models import Occupation, Employee
def jobSearcher(searchArg):
    if searchArg == None:
        return Occupation.id != 0
    else:
        return (Occupation.description.ilike(f"%{searchArg}%")) | (Occupation.name.ilike(f"%{searchArg}%")) \
            | (Occupation.employees.any(Employee.name.ilike(f"%{searchArg}%"))) | (Occupation.employees.any(Employee.email.ilike(f"%{searchArg}%")))