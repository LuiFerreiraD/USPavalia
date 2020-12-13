# open file & create csvreader
import csv, yada yada yada

# import the relevant model
from uspavalia.main.models import Disciplina

#loop:
for line in csv file:
     line = parse line to a list
     # add some custom validation\parsing for some of the fields

     foo = Foo(fieldname1=line[1], fieldname2=line[2] ... etc. )
     try:
         foo.save()
     except:
         # if the're a problem anywhere, you wanna know about it
         print "there was a problem with line", i 