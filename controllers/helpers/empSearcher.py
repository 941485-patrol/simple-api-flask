from models import Employee
def empSearcher(searchArg):
    if searchArg == None:
        return Employee.id != 0
    else:
        return (Employee.email.ilike(f"%{searchArg}%")) | (Employee.name.ilike(f"%{searchArg}%"))