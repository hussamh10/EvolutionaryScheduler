#<parameter name="slotdays">A list of days. Each day is list of slots for that particular day</parameter>
#<parameter name="errorperclash">Fitness to reduce for any clash</parameter>
#<parameter name="errorperload">Fitness to reduce if student is taking three or more courses</parameter>
#<parameter name="courselist">A list of course codes</parameter>
#<parameter name="chromosome">Slot for each course</parameter>
#<parameter name="myfile">Input file containg students and courses data</parameter>
#<summary>Calculate Fitness based upon clashes and overloads</summary>
def fitnessFunction(slotdays, errorperclash, errorperload, courselist, chromosome, myfile):
    
    # Dictionary containing keys as course codes and values as the roll no's registered in that course  
    resigteration = dict()       
    myfields =  []  
    fin = open (myfile, "r")
    allrows = fin.readlines()
    for row in allrows:         
        myfields = row.split(",")
        if myfields[4] in resigteration:
            resigteration[myfields[4]].append(myfiled[1])     
        else:
            resigteration[myfields[4]] = [myfields[1]]

    # Organises chromosome data and sorts courses into particular slots
    slotdiv = []        
    totalslots = 0
    for s in range (len(chromosome)): # find total slots
        if s >= totalslots:
            totalslots = s
    for i in range(totalslots):
        slotdiv.append([])
    for i in range (len(chromosome)):   
        slotdiv[chromosome[i]].append(i)
    
    clashes = 0
    overloads = 0

    # collection with keys as student roll no's and values as the num of courses attempted by that student in a day
    daystudentcoursecount = dict()

    # collection with keys as student roll no's and values as the num of courses attempted by that student in a slot
    studentcoursecount = dict()

    for i in range(len(slotdays)):  # for all days
        daystudentcoursecount = dict()
        for slot in day[i]:             # for all slots in a day
            studentcoursecount = dict()
            for course in slotdiv[slot]:    # for all courses in one slot
                for rollno in resigteration[courselist[course]]:    # for all students registered in a particular course
                    studentcoursecount[rollno] += 1                     # update students courses attempted per slot
                    daystudentcoursecount[rollno] += 1                  # update students courses attempted per day
                    if(studentcoursecount>=2):
                        clashes+=1
        for rollno in daystudentcoursecount:
            if(daystudentcoursecount[rollno] >= 3): # checks if any student is overburdened with courses
                overloads+=(daystudentcoursecount[rollno] - 2)
    
    return 100 - (errorperclash * clashes) - (errorperload * overloads)
