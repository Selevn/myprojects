# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
from Stego import *
from tkinter import messagebox

class Window():
    
    fwhat_in_body = ''
    
    fwhere_in_body = ''
    
    passw = ''    
    
    
    def fwhat_in(self):
        global fwhat_in_body,first
        fwhat_in_body = askopenfilename(filetypes = (("All types", ".*"),))
        if fwhat_in_body != '': self.fwhat_entried['text'] = "✔"
        
    def fwhere_in(self):
        global fwhere_in_body,second
        fwhere_in_body = askopenfilename(filetypes = (("Image files","*.jpg *.png *.bmp"),))
        if fwhere_in_body != '':self.fwhere_entried['text'] = "✔"
    def fwhere_out(self):
        global fwhere_in_body,second
        fwhere_in_body = askopenfilename(filetypes = (("Image files","*.png *.bmp"),))
        if fwhere_in_body != '':self.fwhere_entried['text'] = "✔"
        
    def cont_coding(self):
        global fwhat_in_body,fwhere_in_body,passw
        passw = self.password_input.get()
        if (fwhat_in_body == '') or (fwhere_in_body == ''):
            messagebox.showerror("Ошибка!","Не все файлы выбраны!")
        else:
            self.loading_output = loading(fwhat_in_body,fwhere_in_body)
            self.maked_pas = passmaking(passw)
            if isinstance(self.loading_output, tuple):
                messagebox.showerror(self.loading_output[0],self.loading_output[1])
            elif isinstance(self.maked_pas, tuple):
                messagebox.showerror(self.maked_pas[0],self.maked_pas[1])
            else:
                print(self.loading_output)
                work = coding(*self.loading_output ,  self.maked_pas)
                if work:
                    messagebox.showinfo("Успех!","Файл успешно скрыт!")
    def cont_decoding(self):
        global fwhere_in_body
        if fwhere_in_body == '':
            messagebox.showerror("Ошибка!","Не выбран файл!")
        else:
            passw = self.password_input.get()
            self.maked_pas = passw
            work = decoding(self.maked_pas,fwhere_in_body)
            if isinstance(work,str):
                messagebox.showinfo("Успех!",work)
            elif isinstance(work, tuple):
                messagebox.showerror(work[0],work[1])
        
    def main_mid_frame(self):
        self.mid_frame = Frame(self.my_main_window, bg = 'white',height = '1000')
        self.mid_frame.pack(fill = BOTH)
        
        
        
        
        self.but_coding = Button(self.mid_frame, text = 'Закодировать', font = '29',command=self.codings)
        self.but_encoding = Button(self.mid_frame, text = 'Раскодировать',font = '29',command=self.decodings)
        self.but_coding.place(relx=0.2,rely=0.45)
        self.but_encoding.place(relx=0.6,rely=0.45)
        
    def back(self):
        self.coding_frame.pack_forget()
        self.main_mid_frame()
    
    
    def __init__(self, main_window):
        global fwhat_in_body, fwhere_in_body
        fwhat_in_body = ''
        fwhere_in_body = ''
        self.my_main_window = main_window
        self.top_frame = Frame(self.my_main_window, height = "100",bg = '#c2c2c2')
        self.top_frame.pack(fill = X)
        self.lab1 = Label(self.top_frame, font = 'Arial 32', text = "Стеганография", pady = '30', bg = '#c2c2c2') 
        self.lab1.pack()
        self.main_mid_frame()
    
    
    
    def decodings(self):
        self.mid_frame.pack_forget()
        self.coding_frame = Frame(self.my_main_window, bg = 'white',height = '1000')
        self.coding_frame.pack(fill = BOTH)
        
        self.fwhat_label = Label(self.coding_frame,text = 'Файл-контейнер: ',font = '29',bg = 'white',justify = LEFT)
        self.password_text = Label(self.coding_frame,text = 'Пароль',font = '29' , bg = 'white',justify = LEFT)
        self.password_input = Entry(self.coding_frame, show="•", width='15',bg = "#dbdbdb",font = '23')
        self.fwhat_body = Button(self.coding_frame,text = 'Файл',font = '29', command = self.fwhere_out)
        
        self.fwhere_entried = Label(self.coding_frame,font = '29' , bg = 'white',justify = LEFT)
        self.next_button = Button(self.coding_frame,text = 'Достать',font = '29', command = self.cont_decoding, width = '10')
        self.back_button = Button(self.coding_frame,text = 'Назад',font = '29', command = self.back, width = '10')
        
        self.fwhere_entried.place(relx=0.62,rely=0.1)
        self.fwhat_label.place(relx=0.2,rely=0.1)
        self.password_text.place(relx=0.2,rely=0.3)
        self.password_input.place(relx=0.5,rely=0.3)
        self.fwhat_body.place(relx=0.5,rely=0.1)
        self.next_button.place(relx=0.55,rely=0.5)
        self.back_button.place(relx=0.25,rely=0.5)        
        
        
    def codings(self):
        self.mid_frame.pack_forget()
        self.coding_frame = Frame(self.my_main_window, bg = 'white',height = '1000')
        self.coding_frame.pack(fill = BOTH)
        
        self.fwhat_label = Label(self.coding_frame,text = 'Какой файл: ',font = '29',bg = 'white',justify = LEFT)
        self.fwhere_label = Label(self.coding_frame,text = 'В какой файл: ',font = '29' , bg = 'white',justify = LEFT)
        self.password_text = Label(self.coding_frame,text = 'Пароль',font = '29' , bg = 'white',justify = LEFT)
        
        self.fwhat_entried = Label(self.coding_frame,font = '29' , bg = 'white',justify = LEFT)
        self.fwhere_entried = Label(self.coding_frame,font = '29' , bg = 'white',justify = LEFT)
        self.fwhat_entried.place(relx=0.62,rely=0.1)
        self.fwhere_entried.place(relx=0.62,rely=0.2)
        
        self.next_button = Button(self.coding_frame,text = 'Спрятать',font = '29', command = self.cont_coding, width = '10')
        self.back_button = Button(self.coding_frame,text = 'Назад',font = '29', command = self.back, width = '10')
        
        self.fwhat_body = Button(self.coding_frame,text = 'Файл',font = '29', command = self.fwhat_in)
        self.fwhere_body = Button(self.coding_frame,text = 'Файл',font = '29', command = self.fwhere_in)
        self.password_input = Entry(self.coding_frame, show="•", width='15',bg = "#dbdbdb",font = '23')
        
        
        self.fwhat_label.place(relx=0.2,rely=0.1)
        self.fwhere_label.place(relx=0.2,rely=0.2)
        self.password_text.place(relx=0.2,rely=0.3)
        self.next_button.place(relx=0.55,rely=0.5)
        self.back_button.place(relx=0.25,rely=0.5)
        
        self.fwhere_body.place(relx=0.5,rely=0.2)
        self.fwhat_body.place(relx=0.5,rely=0.1)
        self.password_input.place(relx=0.5,rely=0.3)

root = Tk()

root.title("Стеганография")
root.geometry("600x600")
#root.maxsize(800,800)
#root.minsize(600,500)
root.resizable(False,False)
q = Window(root)
root.mainloop()