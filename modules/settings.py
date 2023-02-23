
def show_settings_window(sg, window_manager):
    settings_window_object = get_settings_window_object(sg, window_manager)
    window = window_manager.make_window(sg, settings_window_object)

    # mainloop
    while True:
        event, values = window.read(timeout=500)
        if event == sg.WIN_CLOSED:
            return True


# internal functions
def get_settings_window_object(sg, window_manager):
    layout = [[sg.Text('This is where the settings will be')]]

    return window_manager.make_window_object(title='Settings', layout=layout, size=(300, 300))
