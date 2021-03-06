import xlrd
import csv
import datetime

def csv_from_excel(myfile,mysheet='Sheet1'):
    wb = xlrd.open_workbook(myfile)
    sh = wb.sheet_by_name(mysheet)
    outputfilename = "readable" + myfile + ".csv"
    #your_csv_file = open(outputfilename, 'wb') # I fixed it but maybe temporarily
    your_csv_file = open(outputfilename, 'w')
    #wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
    wr = csv.writer(your_csv_file)
    
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    
    your_csv_file.close()
 
def xmlconverter():
    
    # Reading basic info
    fin = open("xmlinfo.txt","r")
    giveninfo = fin.readlines()
    myfields = giveninfo[0].split(",")
    fout = open("studentlist.xml","w")
    fout.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\n")
    fout.write("<!--University Course Timetabling-->\n")
    fout.write("<timetable")
    fout.write(" version=\"2.4\"")
    fout.write(" initiative=\"{0}\"".format(myfields[0].strip(' \t\r\n')))
    fout.write(" term=\"{0}\"".format(myfields[1].strip(' \t\r\n')))
    fout.write(" year=\"{0}\"".format(myfields[2].strip(' \t\r\n')))
    fout.write(" created=\"{0}\"".format(datetime.datetime.now()))
    fout.write(" nrDays=\"{0}\"".format(myfields[3].strip(' \t\r\n')))
    fout.write(" slotsPerDay=\"{0}\"".format(myfields[4].strip(' \t\r\n')))
    fout.write(" campus=\"{0}\">\n".format(myfields[0].strip(' \t\r\n')))
    
    # Reading and Inserting Rooms Data into xml file
    myfields = giveninfo[1].split(",")
    csv_from_excel(myfields[0].strip(' \t\r\n'),myfields[1].strip(' \t\n\r'))
    fin = open("readable" + myfields[0].strip(' \t\r\n') + ".csv","r")
    totalrooms = fin.readlines()
    fin.close()
    totalrooms.pop(0)
    it = 0
    while it < len(totalrooms):
        if totalrooms[it] == '\n':
            totalrooms.pop(it)
        else:
            it+=1
    fout.write("\t<rooms>\n")
    for room in totalrooms:
        myfields = room.split(",")
        #print (room) # debugging
        fout.write("\t\t<room id=\"{0}\" constraint=\"true\" capacity=\"{1}\" ignoreTooFar=\"true\"/>\n".format(int(float(myfields[0].strip(' \t\r\n'))),int(float(myfields[2].strip(' \t\r\n')))))
    fout.write("\t</rooms>\n")
    
    # Finding all available combinations of days for any class
    daysallowed = eval(giveninfo[0].split(",")[3].strip(' \t\r\n'))
    daystrings = []
    index = 0
    for i in range(daysallowed - 1):
        for k in range(daysallowed - i - 1):
            daystrings.append("")
            for j in range(i):
                daystrings[index]+="0"
            daystrings[index]+="1"   
            for l in range(k):
                    daystrings[index]+="0"
            daystrings[index]+="1"
            for m in range(7 - len(daystrings[index])):
                daystrings[index]+="0"   
            index+=1
    for i in range(daysallowed):
        daystrings.append("")
        for j in range(i):
            daystrings[index]+="0"
        daystrings[index]+="1"
        for k in range(7 - len(daystrings[index])):
            daystrings[index]+="0"
        index+=1

    # Calculating Time Intervals
    startingtimes = []
    myfields = giveninfo[3].split(",") 
    for i in range(0,len(myfields),2):
        startingtimes.append(int(   ((eval(myfields[i].strip(' \t\r\n')) * 60) + eval(myfields[i+1].strip(' \t\r\n'))) / 5  ))          
      
    #Cleaning Courses Codes from Excel file  
    myfields = giveninfo[2].split(",")
    csv_from_excel(myfields[0].strip(' \t\r\n'),myfields[1].strip(' \t\n\r'))
    fin = open("readable" + myfields[0].strip(' \t\r\n') + ".csv","r")
    myfields.pop(0)  
    myfields.pop(0)     # myfields is a list of values in excel file that are not course codes (headers) 
    myfields[len(myfields)-1]=myfields[len(myfields)-1].strip(' \t\n\r')
    myfields.append("")
    totalcourses = fin.readlines()
    fin.close()
    tempfields = []
    thisisnotacourse = []
    it = 0
    while it < len(totalcourses):
        if totalcourses[it] == '\n':
            totalcourses.pop(it)
        else:
            it+=1
    for course in totalcourses:
        tempfields = course.split(",")
        #print(tempfields)
        if(tempfields[1] in myfields):
            thisisnotacourse.append(course)
    for invalidcourserow in thisisnotacourse:
        totalcourses.remove(invalidcourserow)
    #print(totalcourses) # for debugging purposes
        
    updatedlist = open("updatedcourselist.txt","w")
    fout.write("\t<classes>\n")
    before = []
    after = []
    sections = []
    code = 1  # xml course ids
    instructorid = 1
    instructorlookup = dict()
    for c in range(len(totalcourses)):
        myfields = totalcourses[c].split(")")
        #print(myfields) # for debuggging purposes
        for f in range(2,len(myfields)):
            myfields[1]+=myfields[f]
        #print(myfields[1]) # for debugging purposes
        after = myfields[1].split(",") # I've considered element No.1 as an empty element
        before = myfields[0].split("(")
        sections = before[1].split(",")
        before = before[0].split(",")
        #print(after)
        periodduration = int((eval(after[2].strip(' \t\r\n')) / 2.0) * 12.0)
        for s in sections:
            updatedlist.write(before[0].strip(' \t\r\n') + s.strip(' \t\n\r') + "\n")
            fout.write("\t\t<class id=\"{0}\" offering=\"{0}\" config=\"{0}\" committed=\"false\" subpart=\"{0}\" classLimit=\"{1}\" scheduler=\"0\"".format(code,eval(after[3].split("x")[0].strip(' \t\n\r')))) # i don't know what scheduler meaans
            fout.write(" dates=\"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111\">\n")
            if after[1].strip(' \t\r\n') in instructorlookup:
                fout.write("\t\t\t<instructor id=\"{0}\" solution=\"false\"/>\n".format(instructorlookup[after[1].strip(' \t\r\n')])) # False, right?
            else:
                instructorlookup[after[1].strip(' \t\r\n')] = instructorid
                fout.write("\t\t\t<instructor id=\"{0}\" solution=\"false\"/>\n".format(instructorid)) # False, right?
                instructorid+=1
            for room in totalrooms:
                myfields = room.split(",")
                fout.write("\t\t\t<room id=\"{0}\" pref=\"0\"/>\n".format(int(float(myfields[0].strip(' \t\r\n'))),int(float(myfields[2].strip(' \t\r\n')))))
            for days in daystrings:
                for t in startingtimes:
                    fout.write("\t\t\t<time days=\"{0}\" start=\"{1}\" length=\"{2}\" pref=\"0.0\"/>\n".format(days,t,periodduration))
            fout.write("\t\t</class>\n")
            code+=1
    fout.write("\t</classes>\n")
    updatedlist.close()
    
    fout.write("\t<groupConstraints>\n")
    fout.write("\t</groupConstraints>\n")
    
    # The mapping from course codes to xml course ids
    mycourselistfile = open("updatedcourselist.txt","r")
    courseids = mycourselistfile.readlines()
    mycourselistfile.close()
    #print(courseids)
    courselookup = dict()
    for c in range(len(courseids)):
        courselookup[courseids[c].strip(' \t\n\r')] = c + 1
    totalc = len(courselookup)
        
    # Alloting Student Xml ids to Student Roll No's
    studentnos = open("studentnos.txt","w")
    myfields = giveninfo[4].split(",")
    csv_from_excel(myfields[0].strip(' \t\r\n'),myfields[1].strip(' \t\n\r'))
    studentlist = open("readable" + myfields[0].strip(' \t\r\n') + ".csv","r")
    studentlist = studentlist.readlines() # Just changed the type for ease
    studentlist.pop(0)
    it = 0
    while it < len(studentlist):
        if studentlist[it] == '\n':
            studentlist.pop(it)
        else:
            it+=1 
    givencoursecodes = giveninfo[5].split(",")
    for g in range(len(givencoursecodes)):
        givencoursecodes[g] = givencoursecodes[g].strip(' \t\r\n')
    # Dictionary containing keys as students and values as the courses that student hs registered in
    registeration = dict()       
    for row in studentlist:         
        myfields = row.split(",")
        #print(myfields) # for debugging purposes
        if myfields[3].strip(' \t\n\r') in givencoursecodes:
            #print(myfields[3].strip(' \t\n\r')) # for debugging purposes
            if myfields[1].strip(' \t\r\n') in registeration:
                registeration[myfields[1].strip(' \t\r\n')].append(myfields[4].strip(' \t\r\n') + myfields[6].strip(' \t\r\n'))     
            else:
                registeration[myfields[1].strip(' \t\r\n')] = [myfields[4].strip(' \t\r\n') + myfields[6].strip(' \t\r\n')]
    
    # Writing Students data in xml file
    missingcourseids = []
    fout.write("\t<students>\n")
    newstudentnum = 0
    for r in registeration:
        studentnos.write(str(newstudentnum) + ", " + r)
        fout.write("\t\t<student id=\"{0}\">\n".format(newstudentnum))
        newstudentnum+=1
        for coursetaking in registeration[r]:
            if coursetaking in courselookup:
                fout.write("\t\t\t<class id=\"{0}\"/>\n".format(courselookup[coursetaking]))
            #else: # IF A STUDENT IS TAKING A COURSE THAT IS NOT IN THE INITIAL TIME TABLE COURSE LIST THEN THAT COURSE WONT BE SCHEDULED OR BE CONFLICT FREE
            #    courseids.append(coursetaking+'\n')
            #    missingcourseids.append(coursetaking+'\n')
            #    courselookup[coursetaking] = totalc
            #    fout.write("\t\t\t<class id=\"{0}\"/>\n".format(totalc)) 
            #    totalc+=1
            # A COURSE MUST BE OFFERED, PREREGISTERATIONS OF COURSE NOT OFFERED WILL NOT Be CONSIDERED BECAUSE WE DONT HAVE THE INSTRUCTOR ID OF THESE COURSES !!! 
        fout.write("\t\t</student>\n")
    fout.write("\t</students>\n")
    
    # Updated List of Courses with Missing Courses
    mymissingcourselistfile = open("updatedmissingcourselist.txt","w")
    for mc in missingcourseids:
        mymissingcourselistfile.write(mc)
    
    # Done ! :)
    fout.write("</timetable>\n")
    
xmlconverter()