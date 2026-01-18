
from functions.get_files_info import get_files_info


def print_results(dir_content_list):
    for item in dir_content_list:
        print(f'- {item["name"]} file_size={item["file_size"]}, is_dir={item["is_dir"]}')


dir_contents_list = get_files_info("calculator", ".")
if type(dir_contents_list) is str:
    print(dir_contents_list)
else:
    print_results(dir_contents_list)


dir_contents_list= get_files_info("calculator", "pkg")
if type(dir_contents_list) is str:
    print(dir_contents_list)
else:
    print_results(dir_contents_list)


dir_contents_list = get_files_info("calculator", "/bin")
if type(dir_contents_list) is str:
    print(dir_contents_list)
else:
    print_results(dir_contents_list)


dir_contents_list = get_files_info("calculator", "../")
if type(dir_contents_list) is str:
    print(dir_contents_list)
else:
    print_results(dir_contents_list)
