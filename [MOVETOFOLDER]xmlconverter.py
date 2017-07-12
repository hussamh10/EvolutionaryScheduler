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
    fout.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    fout.write("<!--University Course Timetabling-->")
    fout.write("<timetable")
    fout.write("version=\"2.4\"")
    fout.write("initiative=\"{0}\"".format(myfields[0]))
    fout.write("term=\"{0}\"".format(myfields[1]))
    fout.write("created=\"{0}\"".format(datetime.datetime.now()))
    fout.write("nrDays=\"{0}\"".format(myfields[2]))
    fout.write("slotsPerDay=\"{0}\">".format(myfields[3]))
    
    # Reading and Inserting Rooms Data into xml file
    myfields = giveninfo[1].split(",")
    csv_from_excel(myfields[0],myfields[1].strip(' \t\n\r'))
    fin = open("readable" + myfields[0] + ".csv","r")
    totalrooms = fin.readlines()
    totalrooms.pop(0)
    it = 0
    while it < len(totalrooms):
        if totalrooms[it] == '\n':
            totalrooms.pop(it)
        else:
            it+=1
    fout.write("<rooms>")
    for room in totalrooms:
        myfields = room.split(",")
        #print (room) # debugging
        fout.write("<room id=\"{0}\" constraint=\"true\" capacity=\"{1}\" ignoreTooFar=\"true\"/>".format(myfields[0],myfields[2]))
    fout.write("</rooms>")
    
    # Finding all available combinations of days for any class
    daysallowed = eval(giveninfo[0].split(",")[2])
    daystrings = []
    index = 0
    for i in range(daysallowed - 1):
        for k in range(daysallowed - i - 1):
            daystrings.append("")
            for j in range(i):
                daystrings[index]+="0"
            daystrings[index]+="1"   
            for l in range(k):
                    daystrings+="0"
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
    periodduration = 0
    #atomictime = giveninfo[3].split(",")[0] # You forgot to use this somehow
    myfields = giveninfo[4].split(",")
    shour = eval(myfields[0].strip(' \t\n\r'))
    #print(shour) # for debugging purposes
    smin = eval(myfields[1].strip(' \t\n\r'))
    startinmin = 0
    startinmin = shour * 60
    startinmin += smin
    myfields = giveninfo[5].split(",")
    ehour = eval(myfields[0].strip(' \t\n\r'))
    emin = eval(myfields[1].strip(' \t\n\r'))
    endinmin = 0
    endinmin = ehour * 60
    endinmin += emin 
    startinmin/=5
    endinmin/=5  
      
    #Cleaning Courses Codes from Excel file  
    myfields = giveninfo[2].split(",")
    csv_from_excel(myfields[0],myfields[1].strip(' \t\n\r'))
    fin = open("readable" + myfields[0] + ".csv","r")
    myfields.pop(0)  
    myfields.pop(0)     # myfields is a list of values in excel file that are not course codes (headers) 
    myfields[len(myfields)-1]=myfields[len(myfields)-1].strip(' \t\n\r')
    myfields.append("")
    totalcourses = fin.readlines()
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
    fout.write("<classes>")
    before = []
    after = []
    sections = []
    code = 0  # xml course ids
    instructorid = 0
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
        periodduration = (eval(after[2]) / 2.0) * 12.0
        for s in sections:
            updatedlist.write(before[0] + s.strip(' \t\n\r') + "\n")
            fout.write("<class id=\"{0}\" offering=\"{0}\" config=\"{0}\" committed=\"false\" subpart=\"{0}\" classLimit=\"{1}\" scheduler=\"0\"".format(code,eval(after[3].split("x")[0].strip(' \t\n\r')))) # i don't know what scheduler meaans
            fout.write("dates=\"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111\">")
            if after[1] in instructorlookup:
                fout.write("<instructor id=\"{0}\" solution=\"false\"/>".format(instructorlookup[after[1]])) # False, right?
            else:
                instructorlookup[after[1]] = instructorid
                fout.write("<instructor id=\"{0}\" solution=\"false\"/>".format(instructorid)) # False, right?
                instructorid+=1
            for room in totalrooms:
                myfields = room.split(",")
                fout.write("<room id=\"{0}\" pref=\"0\"/>".format(myfields[0],myfields[2]))
            for days in daystrings:
                for t in range(int(startinmin),int(endinmin-periodduration)):
                    fout.write("<time days=\"{0}\" start=\"{1}\" length=\"{2}\" pref=\"0.0\"/>".format(days,t,periodduration))
            fout.write("</class>")
            code+=1
    fout.write("</classes>")
    updatedlist.close()
    
    # The mapping from course codes to xml course ids
    mycourselistfile = open("updatedcourselist.txt","r")
    courseids = mycourselistfile.readlines()
    #print(courseids)
    courselookup = dict()
    for c in range(len(courseids)):
        courselookup[courseids[c].strip(' \t\n\r')] = c
    totalc = len(courselookup)
        
    # Alloting Student Xml ids to Student Roll No's
    studentnos = open("studentnos.txt","w")
    myfields = giveninfo[6].split(",")
    csv_from_excel(myfields[0],myfields[1].strip(' \t\n\r'))
    studentlist = open("readable" + myfields[0] + ".csv","r")
    studentlist = studentlist.readlines() # Just changed the type for ease
    studentlist.pop(0)
    it = 0
    while it < len(studentlist):
        if studentlist[it] == '\n':
            studentlist.pop(it)
        else:
            it+=1 
    # Dictionary containing keys as students and values as the courses that student hs registered in
    registeration = dict()       
    for row in studentlist:         
        myfields = row.split(",")
        #print(myfields) # for debugging purposes
        if myfields[1] in registeration:
            registeration[myfields[1]].append(myfields[4] + myfields[6])     
        else:
            registeration[myfields[1]] = [myfields[4] + myfields[6]]
    
    # Writing Students data in xml file
    fout.write("<students>")
    newstudentnum = 0
    for r in registeration:
        studentnos.write(str(newstudentnum) + ", " + r)
        fout.write("<student id=\"{0}\">".format(newstudentnum))
        newstudentnum+=1
        for coursetaking in registeration[r]:
            if coursetaking in courselookup:
                fout.write("<class id=\"{0}\"/>".format(courselookup[coursetaking]))
            else: # IF A STUDENT IS TAKING A COURSE THAT IS NOT IN THE INITIAL TIME TABLE COURSE LIST THEN THAT COURSE WONT BE SCHEDULED OR BE CONFLICT FREE
                courseids.append(coursetaking+'\n')
                courselookup[coursetaking] = totalc
                fout.write("<class id=\"{0}\"/>".format(totalc)) 
                totalc+=1
    fout.write("</students>")
    
    # Updated List of Courses with Missing Courses
    mymissingcourselistfile = open("updatedmissingcourselist.txt","w")
    for mc in courseids:
        mymissingcourselistfile.write(mc)
    
    # Done ! :)
    fout.write("</timetable>")
    
xmlconverter()