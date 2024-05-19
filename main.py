import os,json


template_json = {"version":"1.0",
                 "range":100,
                 "inverted":False,
                 "actions":[],
                 "metadata":
                     {
                         "type":"",
                         "description":"",
                         "notes":"",
                         "creator":"",
                         "title":"",
                         "license":"",
                         "performers":[],
                         "tags":[],
                         "script_url":"",
                         "video_url":"",
                         "duration":0
                         }
                 }


def main():
    user_input = input('What directory do you have all your meta files in, please use full path: ')
    diff_directory = os.path.abspath(user_input)
    meta_file_list = get_list_of_files(diff_directory)
    print(f"found {len(meta_file_list)} files to process... processing now")
    for item in meta_file_list:
        process_meta_file(item)

def get_list_of_files(directory=os.getcwd()):
    abs_file_paths_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.meta'):
                abs_file_paths_list.append(os.path.join(root, file))
    return abs_file_paths_list
    

def process_meta_position_data(position_data):
    # action_template = {"pos":0,"at":0}
    funscript_action_list = []
    position_data = position_data.replace("{", "").replace("}","")
    meta_action_list = position_data.split(',')
    for item in meta_action_list:
        item = item.replace('.','')
        item_list = item.split(':')
        temp_funscript_item_dict = {"pos":int(item_list[1])*25,"at":int(item_list[0]+"0")}
        funscript_action_list.append(temp_funscript_item_dict)
    return funscript_action_list
    


def process_meta_file(file_name):
    new_funscript = template_json
    # print(f'processing {file_name}\n')
    meta_file_obj = open(file_name,'r')
    try:
        meta_data = json.load(meta_file_obj)
        meta_file_obj.close()
    except json.decoder.JSONDecodeError as jsondecodeerr:
        print(f"""There was an error decoding a meta file. the following file has issues 
    {file_name}
    You may want to check the file for any issues with the json format, like newlines. there should be only one line.
    Error: {jsondecodeerr}
""")
        quit()
    new_funscript['metadata']['description'] = meta_data['source']
    action_list = process_meta_position_data(meta_data['subs']['text'].replace("{", "").replace("}",""))
    new_funscript['actions'] = action_list
    with open(f'{os.path.splitext(file_name)[0]}.funscript', 'w') as new_funscript_file:
        json.dump(new_funscript, new_funscript_file)

main()