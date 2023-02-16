import json
import PySimpleGUI as sg


def save_data(settings='none', data='none'):
    # create json object from dictionary
    if settings != 'none':
        print(settings)
        settings_json = json.dumps(settings)
        f = open("settings.json", "w")
        f.write(settings_json)
        f.close()
        return True
    elif data != 'none':
        data_json = json.dumps(settings)
        f = open("data.json", "w")
        f.write(data_json)
        f.close()
        return True
    else:
        return False


# Returns data, settings, and main_folder
def get_data(data_type):
    if data_type == 'settings':
        f = open('settings.json', 'r')
    elif data_type == 'data':
        f = open('data.json', 'r')
    data = json.load(f)
    return data


def init_data(data_type):
    if data_type == 'settings':
        data = {
            'general': {'name': 'General', 'value':
                {'style':
                     {'name': 'Theme', 'value': 'DarkGrey11', 'type': 'dropdown', 'choices': sg.theme_list()}
                 }
                        },
            'dev': {'name': 'Dev', 'value':
                {'show':
                     {'name': 'Are you sure you want to show all hidden settings?', 'value': False, 'type': 'checkbox'}
                 }
                    }
        }
    return data
