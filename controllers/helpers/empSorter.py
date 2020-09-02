from models import Employee
def empSorter(sortArg):
    sortKeys=['id', '-id', 'name', '-name', 'email', '-email']
    sort=sortArg
    if sort not in sortKeys:
        return None
    if sort == 'id':
        return Employee.id
    if sort == '-id':
        return Employee.id.desc()
    if sort == 'name':
        return Employee.name
    if sort == '-name':
        return Employee.name.desc()
    if sort == 'email':
        return Employee.email
    if sort == '-email':
        return Employee.email.desc()