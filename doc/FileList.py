import os
import yaml

from doc.names_title import file_name_to_title_name

dir_path = os.path.dirname(os.path.realpath(__file__))

rootdir = '/mnt/c/Users/cmorrow/floobits/share/rmeyer-taos/check-mk-web-api/check_mk_web_api'
generation_list = {}
pages_list = []

for subdir, dirs, files in os.walk(rootdir):
    for file_name in files:
        if 'cpython' in file_name:
            break

        if '__init__' in file_name:
            break

        file_name_list = file_name.split('.py')
        file_name = file_name_list[0]

        pre_file_name = 'check_mk_web_api.'

        file_name2 = file_name + '.md'
        generation_list[file_name2] = pre_file_name + file_name + '+'

        pages_list.append(file_name_to_title_name(file_name))




with open('generate.yml', 'w') as outfile:
    data=  yaml.dump(generation_list, outfile)

with open('pages.yml', 'w') as outfile:
    data = yaml.dump(pages_list, outfile)




