import os
import yaml

dir_path = os.path.dirname(os.path.realpath(__file__))
# file_printer = open('my_file_list', 'w+')
# print
# for each file in the directory,
# print the name of that file
# for x in range(0, 3):
#     file_object.write("We're on time %d" % (x))

rootdir = '/mnt/c/Users/cmorrow/floobits/share/rmeyer-taos/check-mk-web-api/check_mk_web_api'
dict_entry = {}

for subdir, dirs, files in os.walk(rootdir):
    for file_name in files:
        if 'cpython' in file_name:
            break

        if '__init__' in file_name:
            break

        # first_dict_entry = {'activate_mode.md': 'check_mk_web_api.activate_mode+'}

        file_name_list = file_name.split('.py')
        file_name = file_name_list[0]

        pre_file_name = 'check_mk_web_api.'
        # file_printer.write(pre_file_name + file_name + '+')
        # file_printer.write('\n')

        file_name2 = file_name + '.md'
        dict_entry[file_name2] = pre_file_name + file_name + '+'

# After the loop completes,
# we have the first_dict_entry variable
# we want to
# 1) convert the first_dict_entry to yaml
# 2) print the first_dict_entry_yaml to a file

# Keep in mind, you might be able to directly print a python dict
# to a yaml file without doing any weird conversion


# List of pages dict
#
# Format should be name of page
# ie 'Activate Mode'
# value should be name of .md file associated with the title
# ie 'activate_mode.md'
# Full dict entry should look like {'Activate Mode': 'activate_mode.md'}
# https://www.tutorialspoint.com/python/string_title.htm
# I would suggest splitting the string on '_'
# then titleize

# ie file.write(thingie)
with open('data.yml', 'w') as outfile:
    data=  yaml.dump(dict_entry, outfile)



# file_printer.write(data.yaml)
# file_printer.write('\n')
# file_printer.close()


