# This file was written with the help of chatGPT
import os
import csv

class participant:
    def __init__(self, rankings, id, student, slots):
        if(student):
            self.curr_option = 0 
        else:
            self.curr_option = len(rankings)
        self.id = id
        self.rankings = rankings
        self.matched = 0
        self.spots = slots
        self.matched_id = [None] * slots # TODO: fix match algorithm to add/remove proper id


students = []
employers = []

# fill student rankings
student_folder = '/students'

for filename in os.listdir(student_folder):
    file_path = os.path.join(student_folder, filename)
    if os.path.isfile(file_path):
        #open file and fill students
        # Open the CSV file
        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            # Read the contents of the file
            csv_contents = list(reader)

            # Get the first row (headers)
            headers = csv_contents[0]

            # Get the fourth row
            fourth_row = csv_contents[3]

            # Extract the data from the first row for each column that has content on the fourth row
            data = [{"id": headers[i], "rank":fourth_row[i]} for i in range(len(headers)) if fourth_row[i]]
            
            rankings = [None]* (len(data) - 2)
            for i in range(len(data)-2):
                rankings[int(data[i+2]['rank']) - 1] = data[i+2]['id'] 

            students.append(participant(rankings,filename,True,1))

#print(students)

# fill employer rankings
employer_folder  = '/employers'

for filename in os.listdir(student_folder):
    file_path = os.path.join(student_folder, filename)
    if os.path.isfile(file_path):
        #open file and fill employers 
        print("")


cont = True
# loop until all options are exausted for all students 
while cont:  
    cont = False
    for student in students:
        if (not student.matched < student.spots and student.curr_option < len(student.rankings)): # the student is not currently matched go to next option in list
            cont = True # a student is not matched an could have a match so continue the matching process
            
            employer = employers[student.rankings[student.curr_option]] #get net ranked employer

            # if student is ranked higher than the employers current opption then employer and student are tentativly matched
            if(employer.rankings.index(student.id) < employer.curr_option): 
                if(employer.matched == employer.spots):
                    # unset current student matching
                    unmatched_student = students[employer.matched_id]

                    unmatched_student.matched -= 1
                    unmatched_student.curr_option += 1
                    unmatched_student.matched_id = None

                # set match
                employer.matched += 1
                student.matched += 1

                employer.matched_id = student.id
                student.matched_id = employer.id

                employer.curr_option = employer.rankings.index(student.id)

            else:
                # set student to try next option
                student.curr_option += 1


#print matches
for student in students:
    print(student.id, student.matched_id)


#print stats