from functions.write_file_contents import write_file

outcome = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(outcome)

outcome = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(outcome)

outcome = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(outcome)