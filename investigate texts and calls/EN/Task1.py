"""
Intro to Python Project 1, Task 1

Complete each task in the file for that task. Submit the whole folder
as a zip file or GitHub repo.
Full submission instructions are available on the Project Preparation page.
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
TASK 1:
How many different telephone numbers are there in the records?
Print a message:
"There are <count> different telephone numbers in the records."
"""
def amount_telnum(texts,calls):
    telnum_records = []
    for text in texts:
        if text[0] not in telnum_records:
            telnum_records.append(text[0])
        if text[1] not in telnum_records:
            telnum_records.append(text[1])
    for call in calls:
        if call[0] not in telnum_records:
            telnum_records.append(call[0])
        if call[1] not in telnum_records:
            telnum_records.append(call[1])
    return len(telnum_records)

print("There are {} different telephone numbers in the records.".format(amount_telnum(texts,calls)))
