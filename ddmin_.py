import sys, outputters
from split import split
from listsets import listminus
from xml.parsers.xmlproc import xmlproc

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

MAX_DEGREE = 5

def ddmin(data, test, n=1):
    isFailed = False
    for i in range(n, MAX_DEGREE):
        subsets = split(data, i)
        for subset in subsets:
            if test(subset) == FAIL:
                isFailed = True
                return ddmin(subset, test, 2)

    return gettempfiledata()  
        
if __name__ == "__main__":
    tests = {}
    warnings=1
    entstack=0
    rawxml=0

    if len(sys.argv) < 2: 
        print 'Please input file'
        sys.exit()

    fname = sys.argv[1]
    file = open(fname, 'r')
    data = file.read()
    file.close() 

    app = xmlproc.Application()
    p = xmlproc.XMLProcessor()  
    p.set_application(app)
    err=outputters.MyErrorHandler(p, p, warnings, entstack, rawxml)
    p.set_error_handler(err)

    def getfile(s):
        tempfile = open('temp.xml', 'w+')
        tempfile.truncate() 
        tempfile.write(s)
        tempfile.flush()
        tempfile.close()
        return tempfile.name

    def gettempfiledata():
        tempfile = open("temp.xml", 'r')
        data = tempfile.read()
        tempfile.close()
        return data

    def test(c):
        global tests
 
        s = ""
        for char in c:
            s += char

        if s in tests.keys():
            return tests[s]

        try:
            p.set_data_after_wf_error(0)
            p.parse_resource(getfile(c))
            if err.errors == 0:
                print PASS
                tests[s] = PASS
                return PASS
            else:
                print UNRESOLVED
                tests[s] = UNRESOLVED
                return UNRESOLVED
        except UnboundLocalError:
            print FAIL   
            tests[s] = FAIL
            return FAIL

   
    test(data)
    failed =  ddmin(data, test)
    output = "Congratulation! No failed input!"
    for i in tests.values():
        if i == FAIL:
            output = failed
            break
    print '##### The failed input #####\n'
    print output
    print '\n############################'
   
   


   
   



  



