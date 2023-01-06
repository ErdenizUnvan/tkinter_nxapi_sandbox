import requests
import urllib3
from tkinter import *
import tkinter.font as font
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import time
import os
import json
from datetime import datetime
import sys
from tkinter import filedialog
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import json
import requests
import urllib3

global cihazlar
#global cihazlar_combo

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cihazlar=[]
root= Tk()
root.geometry('250x150')
root.configure(bg='#262626')
root.resizable(0,0)
root.title('NXAPI')

def select_file():
    #global dosya_sub_btn
    #global cihazlar
    global cihazlar_combo
    filetypes = (
        ('json files', '*.json'),
    )


    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
    if filename=='':
        showinfo(title='Dosya Seçilmedi',message='Lütfen devam etmek için JSON dosyası seçin')
    else:

        with open(filename) as f:
            devices=json.load(f)
        cihazlar=[]
        if type(devices)==list:
            for device in devices:
                if 'device_type' in device and 'ip' in device:
                    if device['device_type']=='cisco_nxos':
                        cihazlar.append(device['ip'])

            if len(cihazlar)==0:
                showinfo(title='NXOS Yok ',message=f'{filename} içinde cihaz tipi NXOS olan cihaz yok.')
            else:
                
                if dosya_sub_btn:
                    dosya_sub_btn.destroy()
                cihazlarx=' ,'.join(cihazlar)
                nxapi_frame.place_forget()
                root.geometry('900x300')
                nxapi_frame2.place(x=0,y=0)
                cihazlar_combo = ttk.Combobox(nxapi_frame2, value=cihazlar,font=helv36,width=14)
                cihazlar_combo.current(0)
                cihazlar_combo.place(x=140,y=50)

        elif type(devices)==dict:
            if 'device_type' in devices and 'ip' in devices:
                if devices['device_type']=='cisco_nxos':
                    cihazlar.append(devices['ip'])

            if len(cihazlar)==0:
                showinfo(title='NXOS Yok ',message=f'{filename} içinde cihaz tipi NXOS olan cihaz yok.')
            else:
                
                if dosya_sub_btn:
                    dosya_sub_btn.destroy()
                cihazlarx=' ,'.join(cihazlar)
                nxapi_frame.place_forget()
                root.geometry('900x300')
                nxapi_frame2.place(x=0,y=0)
                cihazlar_combo = ttk.Combobox(nxapi_frame2, value=cihazlar,font=helv36,width=14)
                cihazlar_combo.current(0)
                cihazlar_combo.place(x=140,y=50)


        else:
            showinfo(title='NXOS Yok ',message=f'{basename} içinde cihaz tipi NXOS olan cihaz yok.')


def exit():
    root.destroy()

def komut_tipi_sec():
    global rollback_combo_label
    global rollback_combo
    komut_tipi=command_combo.get()
    if komut_tipi=='cli_conf':
        rollback_combo_label.place(x=420,y=90)
        rollback_combo.current(0)
        rollback_combo.place(x=520,y=90)
        json_button.place(x=720,y=180)
        command_label.place(x=40,y=140)
        command_entry.place(x=120,y=140)            

    else:
        if rollback_combo_label:
            rollback_combo_label.place_forget()
        if rollback_combo:
            rollback_combo.place_forget()
        if json_button:
            json_button.place_forget()
        showinfo(title='Komut Tipi ',message=f'Seçilen Komut Tipi: {komut_tipi}')
        command_label.place(x=40,y=140)
        command_entry.place(x=120,y=140)
        json_button.place(x=720,y=180)

def clear_text():
   command_entry.delete(0, END)

def jsona_cevir():
    #global cihazlar_combo

    cihaz=cihazlar_combo.get()
    command_type=command_combo.get()
    rollback=rollback_combo.get()
    #showinfo(title=rollback,message=f'{cihaz},{rollback},{command_type}')
    komut=command_entry.get()
    if komut=='' or komut== ' ' or komut =='  ':
        showinfo(title='Komut yok!',message='Komut yok! Lütfen komut yazın.')

    else:
        if ',' in komut:
            commands=[]
            komutlar=komut.split(',')
            for komut in komutlar:
                commands.append(komut.lstrip())

        else:
            commands=[]
            commands.append(komut)
        if command_type=='cli_conf':
            request_body = {"ins_api": {"version": "1.0",
                            "type": command_type,
                            "chunk": "0",
                            "sid": "1",
                            "input": " ;".join(commands),
                            "output_format": "json",
                            "rollback":rollback}}
            konfig_button.place(x=720,y=220)

            username_label.place(x=40,y=180)
            username_entry.place(x=150,y=180)
            password_label.place(x=40,y=220)
            password_entry.place(x=150,y=220)

            new_window = Toplevel(root)
            new_window.title("JSON olarak Output")             
            text = json.dumps(request_body, indent=4)
            sb = tk.Scrollbar(new_window)
            sb.pack(side='right', fill='y')
            txt = tk.Text(new_window, font="Times32")
            txt.pack()
            txt.config(yscrollcommand=sb.set)
            sb.config(command=txt.yview)
            txt.insert('end', text)

        else:
            request_body = {"ins_api": {"version": "1.0",
                            "type": command_type,
                            "chunk": "0",
                            "sid": "1",
                            "input": " ;".join(commands),
                            "output_format": "json"}}
            konfig_button.place(x=720,y=220)

            username_label.place(x=40,y=180)
            username_entry.place(x=150,y=180)
            password_label.place(x=40,y=220)
            password_entry.place(x=150,y=220)
            new_window = Toplevel(root)
            new_window.title("JSON olarak Output")               
            text = json.dumps(request_body, indent=4)
            sb = tk.Scrollbar(new_window)
            sb.pack(side='right', fill='y')
            txt = tk.Text(new_window, font="Times32")
            txt.pack()
            txt.config(yscrollcommand=sb.set)
            sb.config(command=txt.yview)
            txt.insert('end', text)


def configuration():
    cihaz=cihazlar_combo.get()
    command_type=command_combo.get()
    rollback=rollback_combo.get()
    #showinfo(title=rollback,message=f'{cihaz},{rollback},{command_type}')
    komut=command_entry.get()
    username=username_entry.get()
    password=password_entry.get()

    if komut=='' or komut== ' ' or komut =='  ':
        showinfo(title='Komut yok!',message='Komut yok! Lütfen komut yazın.')

    elif username =='' or password =='' or username ==' ' or password ==' ' or username =='  ' or password =='  ':
        showinfo(title='Yanlış Veri',message='Lütfen kullanıcı adı ve şifreyi doğru yazın')


    else:
        if ',' in komut:
            commands=[]
            komutlar=komut.split(',')
            for komut in komutlar:
                commands.append(komut.lstrip())

        else:
            commands=[]
            commands.append(komut)
        if command_type=='cli_conf':
            try:
                request_body = {"ins_api": {"version": "1.0",
                                "type": command_type,
                                "chunk": "0",
                                "sid": "1",
                                "input": " ;".join(commands),
                                "output_format": "json",
                                "rollback":rollback}}
                response= requests.post(f'https://{cihaz}/ins',
                            auth=(username, password),
                            data=json.dumps(request_body),
                            headers={'content-type': 'application/json'},
                            verify=False,
                            timeout=200)

                if response.json():
                    new_window = Toplevel(root)
                    new_window.title("JSON olarak Output")             
                    text = json.dumps(response.json(), indent=4)
                    sb = tk.Scrollbar(new_window)
                    sb.pack(side='right', fill='y')
                    txt = tk.Text(new_window, font="Times32")
                    txt.pack()
                    txt.config(yscrollcommand=sb.set)
                    sb.config(command=txt.yview)
                    txt.insert('end', text)
                    clear_text()
                
            except Exception as e:
                new_window = Toplevel(root)
                new_window.title("JSON olarak Output")             
                hata={'Sonuc':'Hata','Exception':f'{e}'}           
                text = json.dumps(hata, indent=4)
                sb = tk.Scrollbar(new_window)
                sb.pack(side='right', fill='y')
                txt = tk.Text(new_window, font="Times32")
                txt.pack()
                txt.config(yscrollcommand=sb.set)
                sb.config(command=txt.yview)
                txt.insert('end', text)
                


        else:
            try:
                request_body = {"ins_api": {"version": "1.0",
                                "type": command_type,
                                "chunk": "0",
                                "sid": "1",
                                "input": " ;".join(commands),
                                "output_format": "json"}}

                response= requests.post(f'https://{cihaz}/ins',
                        auth=(username, password),
                        data=json.dumps(request_body),
                        headers={'content-type': 'application/json'},
                        verify=False,
                        timeout=200)
                if response.json():
                    new_window = Toplevel(root)
                    new_window.title("JSON olarak Output")             
                    text = json.dumps(response.json(), indent=4)
                    sb = tk.Scrollbar(new_window)
                    sb.pack(side='right', fill='y')
                    txt = tk.Text(new_window, font="Times32")
                    txt.pack()
                    txt.config(yscrollcommand=sb.set)
                    sb.config(command=txt.yview)
                    txt.insert('end', text)
                    clear_text()

            except Exception as e:
                new_window = Toplevel(root)
                new_window.title("JSON olarak Output")  
                hata={'Sonuc':'Hata','Exception':f'{e}'}           
                text = json.dumps(hata, indent=4)
                sb = tk.Scrollbar(new_window)
                sb.pack(side='right', fill='y')
                txt = tk.Text(new_window, font="Times32")
                txt.pack()
                txt.config(yscrollcommand=sb.set)
                sb.config(command=txt.yview)
                txt.insert('end', text)
      


helv36 = font.Font(family='Helvetica',size=16, weight='bold')
helv38 = font.Font(family='Helvetica',size=10, weight='bold')

nxapi_frame = Frame(root,width=250, height=250,bg='#66ccff')
nxapi_frame.place(x=0,y=0)

dosya_sub_btn=Button(nxapi_frame,text='DOSYA SEÇ',width=10,height=1,fg='white',border=0,bg='#66ccff',command=select_file)
dosya_sub_btn['font']=helv36
dosya_sub_btn.place(x=60,y=30)

cikis = Button(nxapi_frame,text='ÇIKIŞ',width=10,height=1,fg='white',border=0,bg='#66ccff',command=exit)
cikis['font']=helv36
cikis.place(x=60,y=80)

nxapi_frame2 = Frame(root,width=900, height=300,bg='#66ccff')

cihazlar_combo_label = Label(nxapi_frame2, text = 'Cihazlar:',font=helv36,fg="white",bg='#66ccff')
cihazlar_combo_label.place(x=40,y=50)
#cihazlar_combo = ttk.Combobox(nxapi_frame2, font=helv36,width=14)  

cihazlar_combo = ttk.Combobox(nxapi_frame2, value=cihazlar,font=helv36,width=14)

command_combo_label = Label(nxapi_frame2, text = 'Komut Tipi:',font=helv36,fg="white",bg='#66ccff')
command_combo_label.place(x=40,y=90)                

command_type_valid_values = ['cli_show', 'cli_show_array', 'cli_show_ascii', 'cli_conf',  'bash']
command_combo = ttk.Combobox(nxapi_frame2, value=command_type_valid_values,font=helv36,width=13)
command_combo.current(0)
command_combo.place(x=160,y=90)

komut_button = Button(nxapi_frame2,text='SEÇ',width=4,height=1,fg='white',border=0,bg='#66ccff',command=komut_tipi_sec)
komut_button['font']=helv36
komut_button.place(x=340,y=90)

rollback_combo_label = Label(nxapi_frame2, text = 'Rollback:',font=helv36,fg="white",bg='#66ccff')    

rollback_valid_values = ['stop-on-error', 'continue-on-error', 'rollback-on-error']
rollback_combo = ttk.Combobox(nxapi_frame2, value=rollback_valid_values,font=helv36,width=15)                

json_button = Button(nxapi_frame2,text="JSON'a Çevir",width=10,height=1,fg='white',border=0,bg='#66ccff',command=jsona_cevir)
json_button['font']=helv36

cikis = Button(nxapi_frame2,text='ÇIKIŞ',width=10,height=1,fg='white',border=0,bg='#66ccff',command=exit)
cikis['font']=helv36
cikis.place(x=500,y=50)

command_label = Label(nxapi_frame2, text = 'Komut:',font=helv36,fg="white",bg='#66ccff')
 
command_entry = Entry(nxapi_frame2,width=60,font=helv36)


username_label = Label(nxapi_frame2, text = 'Username:',font=helv36,fg="white",bg='#66ccff')
 
username_entry = Entry(nxapi_frame2,width=10,font=helv36)

password_label = Label(nxapi_frame2, text = 'Password:',font=helv36,fg="white",bg='#66ccff')
 
password_entry = Entry(nxapi_frame2,width=10,font=helv36)
password_entry['show'] = '*'


konfig_button = Button(nxapi_frame2,text="POST",width=10,height=1,fg='white',border=0,bg='#66ccff',command=configuration)
konfig_button['font']=helv36


root.mainloop()