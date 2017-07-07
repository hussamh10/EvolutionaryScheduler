class student:
    def __init__(self, line):
        self.parse(line)
        pass

    def parse(self, line):
        line = line.split(',')
        self.sr_no = line[0]
        self.roll_no = line[1]
        self.name = line[2]
        self.degree = line[3]
        self.course_id = line[4]
        self.course_title = line[5]
        self.section = line[6]
        self.teacher = line[7]

    def print(self):
        print(self.sr_no, self.roll_no, self.name, self.degree, self.course_id, self.course_title, self.section, self.teacher)

def main():
    rows = []

    csv = open('file.csv', 'r')
    lines = csv.readlines()

    for line in lines:
        rows.append(student(line))

    for r in rows:
        r.print()

main()
