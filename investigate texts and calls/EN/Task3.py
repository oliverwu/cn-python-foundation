"""
Intro to Python Lab 1, Task 3

Complete each task in the file for that task. Submit the whole folder
as a zip file or GitHub repo.
Full submission instructions are available on the Lab Preparation page.
"""

"""
Read file into texts and calls.
It's ok if you don't understand how to read files
You will learn more about reading files in future lesson
"""
import csv

with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
TASK 3:
(080) is the area code for fixed line telephones in Bangalore.
Fixed line numbers include parentheses, so Bangalore numbers
have the form (080)xxxxxxx.)

Part A: Find all of the area codes and mobile prefixes called by people
in Bangalore.
 - Fixed lines start with an area code enclosed in brackets. The area
   codes vary in length but always begin with 0.
 - Mobile numbers have no parentheses, but have a space in the middle
   of the number to help readability. The prefix of a mobile number
   is its first four digits, and they always start with 7, 8 or 9.
 - Telemarketers' numbers have no parentheses or space, but they start
   with the area code 140.

Print the answer as part of a message:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
The list of codes should be print out one per line in lexicographic order with no duplicates.

Part B: What percentage of calls from fixed lines in Bangalore are made
to fixed lines also in Bangalore? In other words, of all the calls made
from a number starting with "(080)", what percentage of these calls
were made to a number also starting with "(080)"?

Print the answer as a part of a message::
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
The percentage should have 2 decimal digits
"""
def find_fixedline(calls,area_code):
    import re
    amount_of_fixedlines = []
    fixedlines = []
    for call in calls:
        if area_code in call[0] and not(call[1] in amount_of_fixedlines):
            amount_of_fixedlines.append(call[1])
    for fixedline in amount_of_fixedlines:
        if fixedline[0] == "(" and not ((re.match(".*\((.*)\).*",fixedline)).group(1) in fixedlines):
            fixedlines.append((re.match(".*\((.*)\).*",fixedline)).group(1))
        if fixedline[0] == "7" and not (fixedline[0:3] in fixedlines):
            fixedlines.append(fixedline[0:3])
        if fixedline[0] == "8" and not (fixedline[0:3] in fixedlines):
            fixedlines.append(fixedline[0:3])
        if fixedline[0] == "9" and not (fixedline[0:3] in fixedlines):
            fixedlines.append(fixedline[0:3])
        if fixedline[0:2] == "140" and not (fixedline[0:2] in fixedlines):
            fixedlines.append(fixedline[0:2])
    return '\n'.join(sorted(fixedlines))
    # m = re.match(".*\((.*)\).*",amount_of_fixedlines[2])
    # print(amount_of_fixedlines)
    # return m.group(1)
    # return '\n'.join(sorted(amount_of_fixedlines))
print(find_fixedline(calls,'(080)'))
print("The numbers called by people in Bangalore have codes:\n{}".format(find_fixedline(calls,'(080)')))

def find_same_fixedline(calls,area_code):
    # amount_of_same_fixedlines = []
    num_of_same_fixedlines = 0
    for call in calls:
        if area_code in call[0] and area_code in call[1]:
            # amount_of_same_fixedlines.append(call[0])
            # print(len(amount_of_same_fixedlines))
            num_of_same_fixedlines += 1
            # print(num_of_same_fixedlines)
    return num_of_same_fixedlines

# print(find_same_fixedline(calls,'(080)'))

def perc_of_same_fixedline(calls,area_code):
    num_of_same_fixedlines = find_same_fixedline(calls,'(080)')
    num_of_calls = len(calls)
    perc = float(num_of_same_fixedlines/num_of_calls)
    perc = round(perc,2)
    return perc
# print(perc_of_same_fixedline(calls,'(080)'))
print("{} percent of calls from fixed lines in Bangalore are calls to other fixed lines in Bangalore.".format(perc_of_same_fixedline(calls,'(080)')))
