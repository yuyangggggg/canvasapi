import requests
import pandas as pd
from canvasapi import Canvas

# Canvas API URL
API_URL = "https://q.utoronto.ca"
# API_URL = "https://q.utoronto.ca/api/v1"

# Canvas API key
API_KEY = ""


if __name__ == '__main__':
    canvas = Canvas(API_URL, API_KEY)

    courses = canvas.get_courses()
    for course in courses:
        print(course)  # obtain relevant course number

    course = canvas.get_course(233824)  # fill in with course number

    # initialize dictionary with user:assignment status pairs
    data = {}
    enrolled_students = course.get_enrollments(type='StudentEnrollment')

    # get a list of all assignments from course
    assignments = course.get_assignments()
    num_assignments = len(assignments)
    a = [None]*(num_assignments + 1)
    a[0] = "Name"  # store assignment names in a for naming df columns
    for user in enrolled_students:
        data[user.userid] = [None]*num_assignments

    for i in range(num_assignments):
        # inspect each assignment for associated submissions
        assignment = assignments[i]
        a[i+1] = assignment.name
        submissions = assignment.get_submissions()  # returns Paginated List
        # update which users submitted the work in data
        for submission in submissions:
            current_user = submission.userid
            data[current_user][i+1] = True

    # add data to table
    df = pd.DataFrame.from_dict(data, columns=a)
    # sorting
    # sorted_df = df.sort_values(by=['Column_name'], descending=True)

    # send messages to those who have not submitted
