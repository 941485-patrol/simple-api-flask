from models import Occupation
def jobSearcher(searchArg):
    if searchArg == None:
        return Occupation.id != 0
    else:
        return (Occupation.description.ilike(f"%{searchArg}%")) | (Occupation.name.ilike(f"%{searchArg}%"))