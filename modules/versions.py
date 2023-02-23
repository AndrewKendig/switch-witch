
def show_versions_window(sg, os, window_manager, files_manager, group_folder):

    layout = [[sg.Text(group_folder), sg.Button('Refresh')],
              [sg.InputText(key='-NAME-')],
              [sg.Button('Create')],
              [sg.Multiline(key='-VERSIONS-', size=(300, 100), disabled=True)]]

    versions_window_object = window_manager.make_window_object(title='Versions Manager', layout=layout, size=(300, 300))

    window = window_manager.make_window(sg, versions_window_object)

    # mainloop
    while True:
        event, values = window.read(timeout=500)
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Create':
            make_version(os, files_manager, (group_folder + 'Versions\\' + values['-NAME-'] + '\\'))
            update_list(window, files_manager.get_versions(os, group_folder))
            window.Element('-NAME-').Update(value='')
        elif event == 'Refresh':
            update_list(window, files_manager.get_versions(os, group_folder))

    return True


# internal functions
def make_version(os, files_manager, path):
    images_folder, texts_folder = files_manager.init_version_structure(os, path)
    return images_folder, texts_folder


def update_list(window, versions):
    out = ''
    for entry in versions:
        out += entry + '\n'
    window.Element('-VERSIONS-').Update(value=out)
    return True
