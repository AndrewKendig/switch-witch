
def show_groups_window(sg, os, window_manager, files_manager, data_path):

    layout = [[sg.Text(data_path), sg.Button('Refresh')],
              [sg.InputText(key='-NAME-')],
              [sg.Button('Create')],
              [sg.Multiline(key='-GROUPS-', size=(300, 100), disabled=True)]]

    groups_window_object = window_manager.make_window_object(title='Groups Manager', layout=layout, size=(300, 300))

    window = window_manager.make_window(sg, groups_window_object)

    # mainloop
    while True:
        event, values = window.read(timeout=500)
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Create':
            make_group(os, files_manager, (data_path + values['-NAME-'] + '\\'))
            update_list(window, files_manager.get_groups(os, data_path))
            window.Element('-NAME-').Update(value='')
        elif event == 'Refresh':
            update_list(window, files_manager.get_groups(os, data_path))

    return True


# internal functions
def make_group(os, files_manager, path):
    output_folder, versions_folder = files_manager.init_group_structure(os, path)
    return output_folder, versions_folder


def update_list(window, groups):
    out = ''
    for entry in groups:
        out += entry + '\n'
    window.Element('-GROUPS-').Update(value=out)
    return True
