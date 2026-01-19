
from functions.get_files_info import get_files_info


dir_contents_list = get_files_info("calculator", ".")
if type(dir_contents_list) is str:
    print(dir_contents_list)


dir_contents_list= get_files_info("calculator", "pkg")
if type(dir_contents_list) is str:
    print(dir_contents_list)


dir_contents_list = get_files_info("calculator", "/bin")
if type(dir_contents_list) is str:
    print(dir_contents_list)


dir_contents_list = get_files_info("calculator", "../")
if type(dir_contents_list) is str:
    print(dir_contents_list)
