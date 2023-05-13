

class participant:
    def __init__(self, rankings, id, student):
        if(student):
            self.curr_option = 0 
        else:
            self.curr_option = len(rankings)
        self.id = id
        self.rankings = rankings
        self.matched = False
        self.matched_id = None


students = []
employers = []

# fill student rankings


# fill employer rankings

cont = True
# loop until all options are exausted for all students 
while cont:  
    cont = False
    for student in students:
        if (not student.matched and student.curr_option < len(student.rankings)): # the student is not currently matched go to next option in list
            cont = True # a student is not matched an could have a match so continue the matching process
            
            employer = employers[student.rankings[student.curr_option]] #get net ranked employer

            # if student is ranked higher than the employers current opption then employer and student are tentativly matched
            if(employer.rankings.index(student.id) < employer.curr_option): 
                if(employer.matched):
                    # unset current student matching
                    unmatched_student = students[employer.matched_id]

                    unmatched_student.matched = False
                    unmatched_student.curr_option += 1
                    unmatched_student.matched_id = None

                # set match
                employer.matched = True
                student.matched = True

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