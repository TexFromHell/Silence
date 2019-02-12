#
# ................................................................
from tkinter import messagebox
import main
import smtplib

count_attempts = 3


# This function has a purpose to check if user has entered details correctly.
def user_check(args):

    global count_attempts

    # create variable for correct user details.
    correct_username = 'q'
    correct_password = 'q'

    # return user login input values.
    user = main.entry_username.get()
    password = main.entry_password.get()

    # if users username and password entry inputs have no values do nothing.
    if user == "" and password == "":
        return

    # if users input of username and password is correct, open the program.
    if user == correct_username and password == correct_password:
        print('Access Granted !')
        main.window.destroy()
        main.main_screen()

    # if users input of username and password is wrong, decrease count value by one and display the warning label.
    if user != correct_username or password != correct_password:
        count_attempts -= 1
        main.lbl_fail.config(text="Wrong username or password. " + str(count_attempts) + " tries left.", font=("Helvetica", 8), foreground="red", pady=3)

        # if count number is equal to 0 then close the program.
        if count_attempts == 0:
            messagebox.showwarning('Authorisation Error', 'Login attempt failed. Exiting...')
            exit()


def send_email():

    TO = 'silenciumproject@gmail.com'
    SUBJECT = 'TEST MAIL'
    TEXT = 'Here is a message from python.'

    # Gmail Sign In
    gmail_sender = 'silenciumproject@gmail.com'
    gmail_passwd = 'kanapka123'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print('email sent')
    except:
        print('error sending mail')

    server.quit()

# write remote functions here --------




