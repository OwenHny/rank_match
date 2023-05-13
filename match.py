# This file was written with the help of chatGPT
import os
import csv

NAME_LENGTH = 1

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
        self.matched_ids = [] 


students = []
employers = []

# fill student rankings
student_folder = './students'

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

            rankings = [None]* (len(data) - NAME_LENGTH) # TODO: double check subtraction
            for i in range(len(data)-NAME_LENGTH):
                rankings[int(data[i + NAME_LENGTH]['rank']) - 1] = data[i + NAME_LENGTH]['id'] 

            #students.append(participant(rankings,filename,True,1))
            students.append(participant(rankings,data[0]["rank"] ,True,1))

# fill employer rankings
employer_folder  = './employers'

for filename in os.listdir(employer_folder):
    file_path = os.path.join(employer_folder, filename)
    if os.path.isfile(file_path):
        #open file and fill employers 
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
            
            rankings = [None]* (len(data) - NAME_LENGTH) # TODO: double check subtraction
            for i in range(len(data) - NAME_LENGTH):
                rankings[int(data[i + NAME_LENGTH]['rank']) - 1] = data[i + NAME_LENGTH]['id'] 

            #employers.append(participant(rankings,filename,False,1))
            employers.append(participant(rankings,data[0]["rank"],False,1))


def lowest_rank(rankings, matches):
    low = 0

    index = None
    for student in matches:
        if low < rankings.index(student):
            index = matches.index(student)


    return {'rank':low,'index':index}

def get_employer(id):
    for employer in employers:
        if employer.id == id:
            return employer

cont = True
# loop until all options are exausted for all students 
while cont:  
    cont = False
    for student in students:
        if ((not student.matched) and student.curr_option < len(student.rankings)): # the student is not currently matched go to next option in list
            cont = True # a student is not matched an could have a match so continue the matching process

            #print(student.rankings[student.curr_option]) 
            employer = get_employer(student.rankings[student.curr_option]) #get next ranked employer

            # if student is ranked higher than the employers current opption then employer and student are tentativly matched

            if(student.id in employer.rankings and employer.rankings.index(student.id)  < employer.curr_option): 
                if(employer.matched == employer.spots):
                    # unset current student matching

                    #get lowest ranked student
                    index = lowest_rank(employer.rankings, employer.matched_ids)['index']
                    unmatched_student = students[employer.matched_ids[index]]

                    # unmatch student and progress student to next option
                    unmatched_student.matched -= 1
                    unmatched_student.curr_option += 1

                    #remove match ids
                    unmatched_student.matched_ids.remove(employer.id)
                    employer.matched_ids.remove(unmatched_student.id)

                # set match
                employer.matched += 1
                student.matched += 1

                # hold corresponding ids for match
                employer.matched_ids.append(student.id)
                student.matched_ids.append(employer.id)

                # if the employer has all positions tentativly filled then they would brake a match if the student is ranked higher than their current options
                # if employer does not have all positions filled they will take any ranked student
                if(employer.matched == employer.spots):
                    employer.curr_option = lowest_rank(employer.rankings, employer.matched_ids)['rank']

            else:
                # set student to try next option
                student.curr_option += 1


#print matches
for student in students:
    print(student.id, student.matched_ids)

print("\n\n")
for emp in employers:
    print(emp.id, emp.matched_ids)

#print stats