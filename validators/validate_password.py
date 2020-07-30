from wtforms.validators import StopValidation

class ValidatePass():
    def __init__(self):
        self.msg = 'Password must contain at least one number and a capital letter.'

    def __call__(self, form, field):
        upcounter, numcounter = 0,0
        for f in field.data:
            if f.isupper():
                upcounter+=1
            elif f.isdecimal():
                numcounter+=1
            else:
                pass
        if numcounter==0 or upcounter==0:
            raise StopValidation(self.msg)
        