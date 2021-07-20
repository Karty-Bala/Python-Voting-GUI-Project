from PIL import ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sqltor
import matplotlib.pyplot as plt
import sys
import pywhatkit
import datetime
system_time = datetime.datetime.now()
conn = sqltor.connect('team_leader_election.db')
# main cursor
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS poll
                    (name)""")
vote = ['sit20co029', 'sit20co033', 'sit20co013', 'sit20co001', 'sit20co049']
voted = []


def results():
    def back_func():
        res.destroy()
        main_window()

    def send_res():
        def cancel_click():
            send_res_wind.destroy()
            sys.exit()

        def num_check(event):
            count_name = cname.get()
            ph_num = num_entry.get()
            count_code = '0'
            if count_name == '-select-':
                return messagebox.showerror('Error', 'select the name of your Country')
            if ph_num == '' or ph_num.isnumeric() is not True or len(ph_num) < 10:
                return messagebox.showerror('Error', 'Enter a valid Phone number')
            else:
                if count_name == 'India +91':
                    count_code = '+91'
                elif count_name == 'France +33':
                    count_code = '+33'
                elif count_name == 'Hong Kong +852':
                    count_code = '+852'
                elif count_name == 'Indonesia +62':
                    count_code = '+62'
                elif count_name == 'Malaysia +60':
                    count_code = '+60'
                elif count_name == 'United States +1':
                    count_code = '+1'
                full_num = count_code + ph_num
                hrs = int(system_time.strftime("%H"))
                mins = int(system_time.strftime("%M"))
                con = sqltor.connect('team_leader_election.db')
                pcursor = con.cursor()
                pcursor.execute('select * from polling')
                # data-raw
                r = pcursor.fetchall()
                info_msg = []
                for j in range(len(r)):
                    data1 = r[j]
                    ndata = data1[0] + ':' + str(data1[1])
                    info_msg.append(ndata)
                msg = '\n'.join(info_msg)
                pywhatkit.sendwhatmsg(full_num, msg, hrs, mins + 2)
                messagebox.showinfo('Results', 'Results has been sent to the provided number')
                send_res_wind.destroy()
                root_main.destroy()

        countries = ['-select-', 'India +91', 'France +33', 'Hong Kong +852', 'Indonesia +62', 'Malaysia +60',
                     'United States +1']
        cname = StringVar()
        send_res_wind = Toplevel()
        send_res_wind.geometry('1000x600')
        send_res_wind.title('')

        send_res_wind.bg = ImageTk.PhotoImage(file='wallp3.jpg')
        send_res_wind.bg_image = Label(send_res_wind, image=send_res_wind.bg).place(x=0, y=0, relwidth=1, relheight=1)
        send_res_wind.resizable(False, False)

        frm_srw = Frame(send_res_wind, bg='white')
        frm_srw.place(x=145, y=120, height=350, width=700)

        Label(frm_srw, text="Send Results in Whatsapp", font=("times new roman", 25, "bold"), fg="blue",
              bg='white').place(
            x=25, y=30)
        num_label = Label(frm_srw, text="Enter Phone Number", font=("Goudy old style", 15, "bold"), fg="blue",
                          bg='white')
        num_label.place(x=280, y=130)
        num_entry = Entry(frm_srw, font=('times new roman', 15), bg='lightgray')
        num_entry.place(x=280, y=160, width=350, height=35)
        lbl_count = Label(frm_srw, text="Country Code:", font=("Goudy old style", 15, "bold"), fg="blue", bg='white')
        lbl_count.place(x=50, y=130)
        txt_count = ttk.Combobox(frm_srw, values=countries, state='readonly', textvariable=cname)
        txt_count.place(x=50, y=160, width=190, height=35)
        cancel_btn = Button(send_res_wind, cursor='hand2', text="Cancel", fg='white', bg='blue',
                            font=('times new roman', 20))
        cancel_btn.place(x=595, y=370, width=180, height=40)
        num_entry.bind('<Return>', num_check)

    def pie_chart_func():
        names = []
        votes = []
        for i in range(len(r)):
            data_res = r[i]
            names.append(data_res[0])
            votes.append(data_res[1])
            plt.title('Poll Result')
        plt.pie(votes, labels=names, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.show()
    # result-page
    sel = 'team_leader_election'
    res = Toplevel()
    res.geometry('900x500')
    res.title('Results!')

    res.bg = ImageTk.PhotoImage(file='wallp3.jpg')
    res.bg_image = Label(res, image=res.bg).place(x=0, y=0, relwidth=1, relheight=1)

    frame_res = Frame(res, bg='white')
    frame_res.place(x=100, y=50, height=400, width=500)

    Label(frame_res, text='Here is the Results!', font='Helvetica 20 bold', fg='blue', bg='white').place(x=60,
        y=20)
    con = sqltor.connect(sel + '.db')
    pcursor = con.cursor()
    pcursor.execute('select * from polling')
    # data-raw
    r = pcursor.fetchall()
    for j in range(len(r)):
        data = r[j]
        Label(frame_res, text=data[0] + ': ' + str(data[1]) + ' votes', font='Helvetica 20 bold', fg='blue', bg='white').place(x=60, y=100+(j * 50), width=275, height=40)
    pie_btn = Button(frame_res, cursor='hand2', command=pie_chart_func, text="Pie Chart", fg='white', bg='blue',
        font=('Helvetica bold', 20))
    pie_btn.place(x=300, y=340, width=180, height=40)
    send_res_btn = Button(frame_res, cursor='hand2', command=send_res, text="Send Results", fg='white', bg='blue',
        font=('Helvetica bold', 20))
    send_res_btn.place(x=300, y=290, width=180, height=40)
    back_btn = Button(res, command=back_func, cursor='hand2', text="Main Page", fg='white', bg='blue',
                      font=('times new roman', 20))
    back_btn.place(x=20, y=7, width=130, height=40)


def voter_login():
    def back_click():
        votlog.destroy()
        main_window()

    def voter_check(event):
        vote_id = txt_voter.get()
        if vote_id in vote:
            if vote_id in voted:
                messagebox.showerror("Error", "YOU HAVE ALREADY VOTED")
                txt_voter.icursor(0)
                txt_voter.delete(0, END)
            else:
                voted.append(vote_id)
                polling_page()
                txt_voter.icursor(0)
                txt_voter.delete(0, END)
        else:
            messagebox.showerror("Error", "YOUR ID DOESN'T EXIST IN REGISTRY!")
            txt_voter.icursor(0)
            txt_voter.delete(0, END)
    votlog = Toplevel()
    votlog.geometry('1000x600')
    votlog.title('VOTER LOGIN')

    votlog.bg = ImageTk.PhotoImage(file='wallp3.jpg')
    votlog.bg_image = Label(votlog, image=votlog.bg).place(x=0, y=0, relwidth=1, relheight=1)
    votlog.resizable(False, False)

    frame_votlog = Frame(votlog, bg='white')
    frame_votlog.place(x=165, y=150, height=300, width=500)

    Label(frame_votlog, text="Voter login Here", font=("times new roman", 35, "bold"), fg="blue", bg='white').place(
        x=85, y=50)
    lbl_voter = Label(frame_votlog, text="Voter ID", font=("Goudy old style", 15, "bold"), fg="blue", bg='white')
    lbl_voter.place(x=90, y=140)
    txt_voter = Entry(frame_votlog, font=('times new roman', 15), bg='lightgray')
    txt_voter.place(x=90, y=170, width=350, height=35)

    cancel_btn = Button(votlog, cursor='hand2', command=back_click, text="Back", fg='white', bg='blue', font=('times new roman', 20))
    cancel_btn.place(x=425, y=370, width=180, height=40)
    txt_voter.bind('<Return>', voter_check)


def admin_login():
    def back_func():
        top.destroy()
        main_window()

    def pass_crct(event):
        if txt_user.get() == 'admin' and txt_pass.get() == 'password':
            results()
            top.destroy()
        else:
            messagebox.showerror("Error", "Invalid Username/Password", parent=top)
            txt_user.icursor(0)
            txt_pass.delete(0, END)
            txt_user.delete(0, END)

    def cancel_func():
        top.destroy()
        sys.exit()
    top = Toplevel()
    top.geometry('1000x600')
    top.title('ADMIN LOGIN')

    top.bg = ImageTk.PhotoImage(file='wallp3.jpg')
    top.bg_image = Label(top, image=top.bg).place(x=0, y=0, relwidth=1, relheight=1)
    top.resizable(False, False)

    frame_login = Frame(top, bg='white')
    frame_login.place(x=150, y=150, height=340, width=500)

    Label(frame_login, text="Login Here", font=("times new roman", 35, "bold"), fg="blue", bg='white').place(x=90,
        y=30)
    Label(frame_login, text="Admin Login Area", font=("Goudy old style", 20, "bold"), fg="blue",
        bg='white').place(x=90, y=100)
    lbl_user = Label(frame_login, text="Username", font=("Goudy old style", 15, "bold"), fg="blue", bg='white')
    lbl_user.place(x=90, y=140)
    txt_user = Entry(frame_login, font=('times new roman', 15), bg='lightgray')
    txt_user.place(x=90, y=170, width=350, height=35)
    txt_user.icursor(0)
    txt_user.focus()
    lbl_pass = Label(frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="blue",
        bg='white')
    lbl_pass.place(x=90, y=210)
    txt_pass = Entry(frame_login, font=('times new roman', 15), bg='lightgray', show='*')
    txt_pass.place(x=90, y=240, width=350, height=35)
    cancel_btn = Button(top, command=cancel_func, cursor='hand2', text="Cancel", fg='white', bg='blue',
        font=('times new roman', 20))
    cancel_btn.place(x=425, y=470, width=180, height=40)
    Label(frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="blue",
          bg='white').place(x=90, y=210)
    back_btn = Button(top, command=back_func, cursor='hand2', text="Back", fg='white', bg='blue',
           font=('times new roman', 20))
    back_btn.place(x=25, y=20, width=120, height=40)
    txt_pass.bind('<Return>', pass_crct)


def polling_page():
    def proceed():
        chose = choose.get()
        print(chose)
        command = 'update polling set votes=votes+1 where name=?'
        pd.execute(command, (chose,))
        pd.commit()
        messagebox.showinfo('Success!', 'You have voted')
        poll_window.destroy()
    choose = StringVar()
    names = []
    # poll database
    plname = 'team_leader_election'
    pd = sqltor.connect(plname+'.db')
    # poll cursor
    pcursor = pd.cursor()
    pcursor.execute('select name from polling')
    data = pcursor.fetchall()
    for i in range(len(data)):
        data1 = data[i]
        ndata = data1[0]
        names.append(ndata)
    print(names)
    poll_window = Toplevel()
    poll_window.geometry('900x500')
    poll_window.title('Polling Page')
    poll_window.resizable(False, False)

    poll_window.bg = ImageTk.PhotoImage(file='wallp3.jpg')
    poll_window.bg_image = Label(poll_window, image=poll_window.bg).place(x=0, y=0, relwidth=1, relheight=1)

    frame_main = Frame(poll_window, bg='white')
    frame_main.place(x=100, y=50, height=400, width=500)

    Label(frame_main, text='Vote for only One Person!!', font='Helvetica 20 bold', fg='blue', bg='white').place(x=60,
        y=20)
    for i in range(len(names)):
        Radiobutton(frame_main, text=names[i], font='Helvetica 22 bold', fg='blue', bg='white', value=names[i], variable=choose).place(x=60, y=100+(i * 50), width=200, height=40)

    poll_btn = Button(frame_main, cursor='hand2', command=proceed, text="Vote", fg='white', bg='blue',
        font=('Helvetica bold', 20))
    poll_btn.place(x=300, y=340, width=180, height=40)


def main_window():
    def divert_ad():
        home.deiconify()
        home.destroy()
        admin_login()
    def divert_voter():
        home.deiconify()
        home.destroy()
        voter_login()
    home = Toplevel()
    home.geometry('1199x600')
    home.title('Voting Program')
    home['bg'] = '#49A'
    home.resizable(False, False)
    home.bg = ImageTk.PhotoImage(file='wallp3.jpg')
    home.bg_image = Label(home, image=home.bg).place(x=0, y=0, relwidth=1, relheight=1)
    frame_main = Frame(home, bg='white')
    frame_main.place(x=340, y=200, height=200, width=500)
    Label(frame_main, text='E-Booth Voting Program', font='Helvetica 24 bold', fg='blue', bg='white').place(x=60,
                                                                                                            y=20)
    Button(frame_main, cursor='hand2', text="Admin Login", command=divert_ad, fg='white', bg='blue',
           font=('Helvetica', 20)).place(x=270, y=100, width=190, height=40)
    Button(frame_main, cursor='hand2', text='Voter Login', command=divert_voter, fg='white', bg='blue',
           font=('Helvetica', 20)).place(x=30, y=100, width=190, height=40)


root_main = Tk()
main_window()
root_main.withdraw()
root_main.mainloop()
