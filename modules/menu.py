import PySimpleGUI as sg


def get_menu():
    menu_key = '-MENUBAR-'
    font_size = '_ 12'
    menu_def = [
        ['&File', ['&Settings', 'E&xit']],
        ['&Manage', ['&Groups', '&Files']],
        ['&Help', ['There is no help']]
    ]
    return sg.Menu(menu_def, tearoff=True, font=font_size, key=menu_key)


def show_settings(settings):
    left_column = []
    right_column = []

    tabs = []

    for tab in settings:
        tabs.append(settings[tab]['name'])
        left_column.append([sg.Button(settings[tab]['name'])])

    layout = [[sg.Column(left_column, element_justification='c', key='-LEFT_COLUMN-'), sg.Column(right_column, key='-RIGHT_COLUMN-')],
              [sg.Button('Save', font='Corbel 14 bold')]]

    window = sg.Window('Settings', layout)

    

    while True:  # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save':
            settings
        elif event in tabs:
            window['-RIGHT_COLUMN-'].update([])
            for tab in settings:
                if settings[tab]['name'] == event:
                    options = settings[tab]['value']
                    for option in options:
                        if options[option]['type'] == 'checkbox':
                            window.extend_layout(
                                window['-RIGHT_COLUMN-'],
                                [[sg.Text(options[option]['name']),
                                 sg.Checkbox(default=options[option]['value'], key='-' + options[option]['Name'] + '-')]]
                            )
                        elif options[option]['type'] == 'dropdown':
                            window.extend_layout(
                                window['-RIGHT_COLUMN-'],
                                [[sg.Text(options[option]['name']),
                                 sg.Combo(options[option]['choices'], key='-' + options[option]['name'] + '-')]]
                            )
                break

    window.close()
    return settings
