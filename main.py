import schoolopy
from datetime import datetime
import os
from dotenv import load_dotenv

now = datetime.now()

load_dotenv("keys.env")

key = os.getenv("key")
secret = os.getenv("secret")
user_id = os.getenv("userid")


# Two-legged
auth = schoolopy.Auth(key, secret)
sc = schoolopy.Schoology(auth)

userProfile = sc._get(f"users/{user_id}/sections")

# print(len(userProfile['section']))

def getassignments(classID): 
    return sc._get(f"sections/{classID}/assignments")

all_assignments = []

for section in userProfile['section']:
    section_id = section['id']
    course_name = section['course_title']

    data = getassignments(section_id)

    for assignment in data['assignment']:
        assignment['course'] = course_name
        all_assignments.append(assignment)


upcoming = [
    assignment
    for assignment in all_assignments
    if assignment['due']
    and datetime.strptime(assignment['due'], "%Y-%m-%d %H:%M:%S") > now
]

upcoming.sort(
    key=lambda x: datetime.strptime(x['due'], "%Y-%m-%d %H:%M:%S")
)



for item in upcoming:

    item['timetodue'] = (datetime.strptime(item['due'], "%Y-%m-%d %H:%M:%S") - now).days

for i in range(len(upcoming)):
    print("-"*20)
    print()
    print("In order of upcoming, this is number " + str((i+1)))
    print()
    print(upcoming[i]['title'] + " IS DUE ON " + upcoming[i]['due'] + "\n FOR CLASS        --->     " + upcoming[i]['course'] + "\n WITH DESCRIPTION --->     " + upcoming[i]['description'])
    print("This us due in    --->     " + str(upcoming[i]['timetodue']) + " days")
    print()
    print()
    print("-"*20)

