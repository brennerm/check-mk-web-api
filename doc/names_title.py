

def file_name_to_title_name(file_name):
    """
    #Arguments
    check_mk_url (str): URL to Check_Mk web application, check file names and print for each file in the directory in the correct format

    #Examples
    file_name_to_title_name('activate_mode')
    output = 'Activate Mode: activate_mode.md'
    """

    file_name_list = file_name.split('.py')
    file_name = file_name_list[0]
    title = file_name.replace('_', ' ').title()
    filename2 = ': ' + file_name + '.md'

    return title + filename2

