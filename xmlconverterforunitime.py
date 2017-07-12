import csv
import xlrd
import datetime

def csv_from_excel(myfile,mysheet='Sheet1'):
    wb = xlrd.open_workbook(myfile)
    sh = wb.sheet_by_name(mysheet)
    outputfilename = "readable" + myfile + ".csv"
    your_csv_file = open(outputfilename, 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
    
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
    fout.write("initiative=\"{0}\"",myfields[0])
    fout.write("term=\"{0}\"",myfields[1])
    fout.write("created=\"{0}\"",datetime.datetime.now())
    fout.write("nrDays=\"{0}\"",myfields[2])
    fout.write("slotsPerDay=\"{0}\">",myfields[3])
    
    # Reading and Inserting Rooms Data into xml file
    myfields = giveninfo[1].split(",")
    csv_from_excel(myfields[0],myfields[1])
    fin = open("readable" + myfields[0] + ".csv","r")
    totalrooms = fin.readlines()
    totalrooms.pop(0)
    fout.write("<rooms>")
    for room in totalrooms:
        myfields = room.split(",")
        fout.write("<room id=\"{0}\" constraint=\"true\" capacity=\"{1}\" ignoreTooFar=\"true\"/>",myfields[0],myfields[2])
    fout.write("</rooms>")
    
    # Finding all available combinations of days for any class
    daysallowed = giveninfo[0].split(",")[2]
    daystrings = []
    index = 0
    for i in range(daysallowed - 1):
        for k in range(daysallowed - i - 1):
            daystrings[index] = ""
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
        daysallowed[index] = ""
        for j in range(i):
            daysallowed[index]+="0"
        daysallowed[index]+="1"
        for k in range(7 - len(daysallowed[index])):
            daysallowed[index]+="0"
        index+=1

    # Calculating Time Intervals
    periodduration = 0
    #atomictime = giveninfo[3].split(",")[0] # You forgot to use this somehow
    myfields = giveninfo[4].split(",")
    shour = myfields[0]
    smin = myfields[1]
    startinmin = shour * 60
    startinmin += smin
    myfields = giveninfo[5].split(",")
    ehour = myfields[0]
    emin = myfields[1]
    endinmin = ehour * 60
    endinmin += emin 
    startinmin/=5
    endinmin/=5  
      
    #Cleaning Courses Codes from Excel file  
    myfields = giveninfo[2].split(",")
    csv_from_excel(myfields[0],myfields[1])
    fin = open("readable" + myfields[0] + ".csv","r")
    myfields.pop(0)  
    myfields.pop(1)     # myfields is a list of values in excel file that are not course codes (headers) 
    totalcourses = fin.readlines()
    tempfields = []
    thisisnotacourse = []
    for course in totalcourses:
        tempfields = totalcourses[i].split(",")
        if(tempfields[1] in myfields):
            thisisnotacourse.append(course)
    for invalidcourserow in thisisnotacourse:
        totalcourses.remove(invalidcourserow)
        
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
        after = myfields[1].split(",") # I've considered element No.1 as an empty element
        before = myfields[0].split("(")
        sections = before[1].split(",")
        before = before[0].split(",")
        periodduration = (eval(after[2]) / 2.0) * 12.0
        for s in sections:
            updatedlist.write(before[0] + s)
            fout.write("<class id=\"{0}\" offering=\"{0}\" config=\"{0}\" committed=\"false\" subpart=\"{0}\" classLimit=\"{1}\" scheduler=\"0\"",code,eval(after[3].split("x")[0])) # i don't know what scheduler meaans
            fout.write("dates=\"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111\">")
            if after[1] in instructorlookup:
                fout.write("<instructor id=\"{0}\" solution=\"false\"/>",instructorlookup[after[i]]) # False, right?
            else:
                instructorlookup[after[1]] = instructorid
                fout.write("<instructor id=\"{0}\" solution=\"false\"/>", instructorid) # False, right?
                instructorid+=1
            for room in totalrooms:
                myfields = room.split(",")
                fout.write("<room id=\"{0}\" pref=\"0\"/>",myfields[0],myfields[2])
            for days in daysallowed:
                for t in range(startinmin,endinmin-periodduration):
                    fout.write("<time days=\"{0}\" start=\"{1}\" length=\"{2}\" pref=\"0.0\"/>",days,t,periodduration)
            fout.write("</class>")
            code+=1
    fout.write("</classes>")
    updatedlist.close()
    
    # The mapping from course codes to xml course ids
    mycourselistfile = open("updatedcourselist.txt","r")
    courseids = mycourselistfile.readlines()
    courselookup = dict()
    for c in range(len(courseids)):
        courselookup[courseids[c]] = c
        
    # Alloting Student Xml ids to Student Roll No's
    studentnos = open("studentnos","w")
    myfields = giveninfo[6].split(",")
    csv_from_excel(myfields[0],myfields[1])
    studentlist = open("readable" + myfields[0] + ".csv","r")
    studentlist.pop(0)
    # Dictionary containing keys as students and values as the courses that student hs registered in
    registeration = dict()       
    for row in studentlist:         
        myfields = row.split(",")
        if myfields[1] in registeration:
            registeration[myfields[1]].append(myfields[4] + myfields[6])     
        else:
            registeration[myfields[1]] = [myfields[4] + myfields[6]]
    
    # Writing Students data in xml file
    fout.write("<students>")
    newstudentnum = 0
    for r in registeration:
        studentnos.write(newstudentnum+", " + registeration[r])
        fout("<student id=\"{0}\">",newstudentnum)
        newstudentnum+=1
        for coursetaking in registeration[r]:
            fout.write("<class id=\"{0}\"/>",courselookup[coursetaking])
    fout.write("</students>")
    
    # Done ! :)
    fout.write("</timetable>")
