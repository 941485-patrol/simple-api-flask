from models import Occupation
def jobSorter(sortArg):
    sortKeys=['id', '-id', 'name', '-name', 'description', '-description']
    sort=sortArg
    if sort not in sortKeys:
        return None
    if sort == 'id':
        return Occupation.id
    if sort == '-id':
        return Occupation.id.desc()
    if sort == 'name':
        return Occupation.name
    if sort == '-name':
        return Occupation.name.desc()
    if sort == 'description':
        return Occupation.description
    if sort == '-description':
        return Occupation.description.desc()