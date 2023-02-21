
def start_window(sg, window):
    title = window['title']
    layout = window['layout']
    size = window['size']
    return sg.Window(title=title, layout=layout, size=size)


def change_theme(sg, theme):
    sg.theme(theme)
    return True


def get_main_window_object(sg):
    menu_def = [
        ['&File', ['&Settings', 'E&xit']],
        ['&Manage', ['&Groups', '&Files']],
        ['&Help', ['There is no help']]
    ]
    menu = get_menu(sg, '-MENUBAR-', 'Corbel 10', menu_def)

    controls = make_frame(sg, [[sg.Text('This is where the controls will be')]], 'Controls', (300, 200))
    text_preview = make_frame(sg, [[sg.Text('This is where text previews will go')]], 'Edit Texts', (300, 300))
    image_preview = make_frame(sg, [[sg.Text('This is where image previews will go')]], 'Images', (250, 500))

    layout = [[menu], [make_column(sg, [[controls], [text_preview]]), make_column(sg, [[image_preview]])]]

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


def get_menu(sg, menu_key, font_size, menu_def):
    return sg.Menu(menu_def, tearoff=True, font=font_size, key=menu_key)
