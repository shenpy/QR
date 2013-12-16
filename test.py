class BA(object):
    initial={'a':'a'}

    def get_initials(self):
        return self.initial.copy()

class BS(BA):

    def get_initials(self):
        initial= super(BS, self).get_initials()
        initial['add']='ass'
        return initial

a = BA()
print a.initial

b = BS()
print b.get_initials()

print a.get_initials()


