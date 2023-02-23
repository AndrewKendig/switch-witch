
def make_window(sg, window):
    title = window['title']
    layout = window['layout']
    size = window['size']
    return sg.Window(title=title, layout=layout, size=size)


def change_theme(sg, theme):
    sg.theme(theme)
    return True


def get_main_window_object(sg, os, data_path, files_manager):
    menu_def = [
        ['&File', ['&Settings', 'E&xit']],
        ['&Manage', ['&Groups', '&Versions', '&Files']],
        ['&Help', ['There is no help']]
    ]
    menu = make_menu(sg, '-MENUBAR-', 'Corbel 10', menu_def)

    layout = [[menu], [make_column(sg, [[make_controls_section(sg, os, data_path, files_manager)], [make_text_preview_section(sg)]]), make_column(sg, [[make_image_preview_section(sg)]])]]

    return make_window_object(title='Switch Witch', layout=layout, size=(600, 500))


def show_not_implemented(sg, webbrowser):
    layout = [[sg.Text('This feature hasn\'t been implemented yet.\nFor updates watch the GitHub page')],
              [sg.Text('Show me the GitHub', enable_events=True, key="GitHub", text_color='deep sky blue')],
              [sg.Text('')],
              [sg.OK('OK')]]
    window = sg.Window(title='Work in Progress', layout=layout, element_justification='c')
    while True:
        event, values = window.read(timeout=500)
        if event == sg.WIN_CLOSED or event == 'OK':
            break
        elif event == "GitHub":
            webbrowser.open("https://github.com/AndrewKendig/switch-witch", new=0, autoraise=True)

    window.close()
    return True


# internal functions

def make_controls_section(sg, os, data_path, files_manager):
    options = files_manager.get_groups(os, data_path)
    group_selector = [[sg.Text('Select Group', font='_ 10 bold')], [sg.Text(' '), sg.Combo(options, size=(20, 1), key="-GROUP-"), sg.Button('Select Group')]]
    version_selector = [[sg.Text('Select Version', font='_ 10 bold')], [sg.Text(' '), sg.Combo([], size=(34, 1), key="-VERSION-")], [sg.Text(' '), sg.Button('Switch to Version', size=(31, 1))]]
    apply_button = [[sg.Button('Apply Changes', size=(36, 2), font="_ 14 bold")]]
    layout = [*group_selector, *version_selector, *apply_button]
    return make_frame(sg, layout, 'Controls', (300, 200))


def make_text_preview_section(sg):
    layout = [[sg.Text('This is where text previews will go')]]
    return make_frame(sg, layout, 'Edit Texts', (300, 300))


def make_image_preview_section(sg):
    layout = [[sg.Text('This is where image previews will go')]]
    return make_frame(sg, layout, 'Images', (250, 500))



def make_window_object(title, layout, size):
    return {
        "title": title,
        "layout": layout,
        "size": size
    }


def make_frame(sg, contents, title, size):
    return sg.Frame(layout=contents, title=title, size=size)


def make_column(sg, contents, justification='l'):
    return sg.Column(contents, element_justification=justification)


def make_menu(sg, menu_key, font_size, menu_def):
    return sg.Menu(menu_def, tearoff=True, font=font_size, key=menu_key)
