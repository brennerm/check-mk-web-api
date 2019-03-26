import os
import yaml

dir_path = os.path.dirname(os.path.realpath(__file__))

rootdir = '/mnt/c/Users/cmorrow/floobits/share/rmeyer-taos/check-mk-web-api/check_mk_web_api'
dict_entry = {}

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
        dict_entry[file_name2] = pre_file_name + file_name + '+'


with open('data.yml', 'w') as outfile:
    data=  yaml.dump(dict_entry, outfile)




