
from tkinter import messagebox
import pytz
from datetime import datetime
from tkinter import *
import requests
tame=pytz.timezone("Asia/Kolkata")
window=Tk()

window.geometry("800x480")
window.resizable(False,False)
window.title("Vaccine checker")
window.config(background='#add8e6')
window.iconbitmap("xx.ico")

subwindow1=Frame(window,width=200,height=140,bg="#00308F",relief=FLAT)
subwindow1.place(x=0,y=0)

subwindow2=Frame(window,width=600,height=140,bg="#007FFF",relief=FLAT)
subwindow2.place(x=200,y=0)

subwindow3=Frame(window,width=800,height=40,bg="#041E42",relief=FLAT)
subwindow3.place(x=0,y=140)

pincode_var=StringVar()
pincode=Entry(window,width=12,font="cursive",bg="#f5f5f5",textvariable=pincode_var)
pincode.place(x=280,y=50)
pincode['textvariable']=pincode_var

date_var=StringVar()
date=Entry(window,width=12,font="cursive",bg="#f5f5f5",textvariable=date_var)
date.place(x=540,y=50)
date['textvariable']=date_var



today=Label(font="cursive 16 bold",text="Current Date",bg="#00308F",fg="white")
today.place(x=35,y=30)

current_time=Label(font="cursive 17",text="Current Time",bg="#00308F",fg="white")
current_time.place(x=40,y=80)

label_pin=Label(font="cursive 12",text="Enter Pincode",bg="#007FFF",fg="white")
label_pin.place(x=296,y=20)

label_date=Label(font="cursive 12",text="Enter Date",bg="#007FFF",fg="white")
label_date.place(x=530,y=20)

label_date=Label(font="cursive 10",text="(dd-mm-yyyy)",bg="#007FFF",fg="white")
label_date.place(x=610,y=21)

label_date=Label(font="cursive 8",text="Search for \nvaccines",bg="#007FFF",fg="white")
label_date.place(x=738,y=80)

label_sta=Label(font="cursive 10",text="Status",bg="#041E42",fg="white")
label_sta.place(x=14,y=148)

label_cen=Label(font="cursive 10",text="Centre",bg="#041E42",fg="white")
label_cen.place(x=110,y=148)

label_vac=Label(font="cursive 10",text="Vaccine",bg="#041E42",fg="white")
label_vac.place(x=280,y=148)

label_age=Label(font="cursive 10",text="Age",bg="#041E42",fg="white")
label_age.place(x=380,y=148)

label_d1=Label(font="cursive 10",text="First Dose",bg="#041E42",fg="white")
label_d1.place(x=440,y=148)

label_d2=Label(font="cursive 10",text="Second Dose",bg="#041E42",fg="white")
label_d2.place(x=550,y=148)

label_tot=Label(font="cursive 10",text="Total vaccines",bg="#041E42",fg="white")
label_tot.place(x=670,y=148)

stat=Text(window,width=10,height=22,bg="#add8e6",font="cursive 10",fg="#000080",relief=FLAT)
stat.place(x=5,y=180)

cent=Text(window,width=32,height=22,bg="#add8e6",font="cursive 10",fg="#000080",relief=FLAT)
cent.place(x=73,y=180)

vac=Text(window,width=15,height=22,bg="#add8e6",font="cursive 10",fg="#000080",relief=FLAT)
vac.place(x=273,y=180)

ag=Text(window,width=9,height=22,bg="#add8e6",font="cursive 10",fg="#000080",relief=FLAT)
ag.place(x=380,y=180)

fd=Text(window,width=13,height=22,bg="#add8e6",font="cursive 10",fg="#000080",relief=FLAT)
fd.place(x=450,y=180)

sd=Text(window,width=13,height=22,bg="#add8e6",font="cursive 10",fg="#000080",relief=FLAT)
sd.place(x=570,y=180)

tl=Text(window,width=13,height=22,bg="#add8e6",font="cursive 10",fg="#000080",relief=FLAT)
tl.place(x=690,y=180)


def clock():
    tim=datetime.now(tame)
    current_date=tim.strftime("%d-%m-%Y")
    current_time1=tim.strftime("%H:%M:%S")
    today.config(text=current_date)
    current_time.config(text=current_time1)
    current_time.after(1000,clock)

clock()

def todaysdate():
    date=datetime.now(tame)
    ans=date.strftime("%d-%m-%Y")
    date_var.set(ans)

today_var=IntVar()
datebox=Checkbutton(window,text="Today",bg="#007FFF",command=todaysdate,variable=today_var,onvalue=1,offvalue=0)
datebox.place(x=580,y=80)

url="https://ipinfo.io/postal"
ans_pin=requests.get(url).text

def autofill_pin():
    pincode_var.set(ans_pin)

location=StringVar()
radio=Radiobutton(window,text="Autofill",bg="#007FFF",variable=location,value=location,command=autofill_pin)
radio.place(x=320,y=82)

def clear():
    #1 means start and end is end
    cent.delete('1.0', END)
    ag.delete('1.0', END)
    tl.delete('1.0', END)
    fd.delete('1.0', END)
    sd.delete('1.0', END)
    vac.delete('1.0', END)
    stat.delete('1.0', END)
    

def api(Pincode,Date):
    header={'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}
    link=f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={Pincode}&date={Date}"
    answer=requests.get(link,headers=header)
    #answer is in json format only
    json_answer=answer.json()
    return json_answer

def results():
    clear()
    # strip clears spaces inbuilt
    Pincode=pincode_var.get().strip()
    Date=date_var.get()
    json_answer=api(Pincode,Date)

    if len(json_answer["sessions"])==0:
        messagebox.showinfo("INFO","No vaccine available")

    for session in json_answer["sessions"]:
        name1=session["name"]
        age=session["min_age_limit"]
        vac_name=session["vaccine"]
        firstdose=session["available_capacity_dose1"]
        seconddose=session["available_capacity_dose2"]
        capacity=session["available_capacity"]

        if capacity>0:
            status="Available"

        if capacity==0:
            status="NA"

        if age==45:
            fage="45+"

        if(age<45):
            fage="18+"

        stat.insert(END,status)
        stat.insert(END,"\n")
        cent.insert(END,name1)
        cent.insert(END,"\n")
        vac.insert(END,vac_name)
        vac.insert(END,"\n")
        ag.insert(END,fage)
        ag.insert(END,"\n")
        fd.insert(END,firstdose)
        fd.insert(END,"\n")
        sd.insert(END,seconddose)
        sd.insert(END,"\n")
        tl.insert(END,capacity)
        tl.insert(END,"\n")
        


search_image=PhotoImage(file="final.png")
# photoimage = search_image.subsample(1, 1)
button=Button(window,bg="#f5f5f5",width=15,height=15,relief="raised",image=search_image,command=results)
button.place(x=755,y=52)





window.mainloop()