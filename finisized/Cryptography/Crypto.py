#coding: utf-8
from tkinter import *
from tkinter.ttk import Combobox, Progressbar
from tkinter.filedialog import *
from tkinter import messagebox
import hashlib

import os


class Main_window():
    def __init__(self, root_window):
        global window
        self.file = ''
        self.window = root_window
        
        self.header = Label(self.window, text = "Криптография",font = 'Arial 20')
        self.header.place(relx = 0.33,rely = 0.05)
        
        self.selectfile_label = Label(self.window, text = "Выберите файл",font = 'Arial 14')
        self.selectfile_label.place(relx = 0.15,rely = 0.25)
        
        self.selectfile_button = Button(self.window, text = "Файл",font = 'Arial 14',command=self.file_choise)
        self.selectfile_button.place(relx = 0.5 ,rely = 0.24)
        
        self.file_entried = Label(self.window,font = 'Arial 24')
        self.file_entried.place(relx = 0.65 ,rely = 0.23)
        
        
        self.key_label = Label(self.window, text = "Введите ключ",font = 'Arial 14')
        self.key_label.place(relx = 0.15,rely = 0.4)
        
        
        self.showkeybutton = Button(self.window, text = "Показать",font = 'Arial 10',command=self.show_hide)
        self.showkeybutton.place(relx = 0.75 ,rely = 0.4)
        
        self.key_entry = Entry(self.window,font = 'Arial 14',width = 10 ,show="•") #
        self.key_entry.place(relx = 0.5 ,rely = 0.4)
        
        self.hash_method_label = Label(self.window, text = "Метод шифрования",font = 'Arial 14')
        self.hash_method_label.place(relx = 0.15 ,rely = 0.55)
        
        self.selectorVal = StringVar()
        
        self.hash_method_list = Combobox(self.window, state='readonly', textvariable = self.selectorVal)
        self.hash_method_list['values'] = ("Без хэширования", "md5", "sha1", "sha256", "sha224", "sha512", "sha3_224", "sha3_256", "sha3_384" ,"sha3_512")
        self.hash_method_list.current(0)
        self.hash_method_list.place(relx = 0.58 ,rely = 0.56)
        
        self.but = Button(self.window, text = "Крипто!",font = 'Arial 14',command=self.doit)
        self.but.place(relx = 0.43 ,rely = 0.67)
        
        self.pbar = Progressbar(self.window, length = 300)
        self.pbar["maximum"]=300
    def show_hide(self):
        if self.showkeybutton['text'] == "Показать":
            self.showkeybutton['text'] = "Скрыть"
            self.key_entry['show'] = ""
        else:
            self.showkeybutton['text'] = "Показать"
            self.key_entry['show'] = "•"
        
    def doit(self):
        self.password = self.key_entry.get()
        if self.password == '':
            messagebox.showerror("Ошибка!","Введите ключ!")
        elif self.file == '':
                messagebox.showerror("Ошибка!","Выберите файл!")
        else:
            self.key = self.key_do(self.password)
            out = self.crypto(self.file, self.key)
            if isinstance(out, str):
                messagebox.showinfo("Готово!","Шифрование к файлу {} успешно применено!".format(out))
        self.pbar['value'] = 0
        self.pbar.place_forget()
            
            
    def crypto(self, file, key):
        dirictory = os.path.dirname(file)
        file_name = os.path.basename(file)
        size = os.path.getsize(file)
        key = str.encode(key)
        try:
            file_body = open(file,'rb')
            output_body = open(dirictory+"//"+os.path.splitext(file_name)[0]+".slvn",'wb')
        except:
            messagebox.showerror("Ошибка!","Невозможно открыть файл!")
            return False
        i = 0
        if size>300:
            perc = round(size/300)#получаем кол-во итераций для одного символа
            self.pbar.place(relx = 0.22 ,rely = 0.85)
        else:
            perc = 0
            
        loading_status = 0
        counter = 0
        for line in file_body:
            for symbol in line:
                out_c = symbol^key[i]
                #out_c = symbol
                i+=1
                if i>=len(key):
                    i = 0
                counter+=1
                if (perc != 0) and counter>perc:
                    #print(loading_status)
                    counter = 0
                    loading_status+=1 #ТУТ СДЕЛАЙ ИТЕРАЦИЮ В СТАТУС БАР
                    self.pbar['value'] = loading_status
                    self.pbar.update()
                    #print(self.pbar['value'])
                #output_body.write(bytearray(out_c))
                output_body.write(out_c.to_bytes(1, byteorder='big'))
        self.pbar['value'] = 300
        file_body.close()
        try:
            os.remove(file)
        except:
            os.remove(dirictory+"//"+os.path.splitext(file_name)[0]+".slvn")
            output_body.close()
            messagebox.showerror("Ошибка!","Не используйте файлы во время кодирования!")
            return False
        output_body.close()
        os.rename(dirictory+"//"+os.path.splitext(file_name)[0]+".slvn", file)
        
        return file_name
        
        
        
    def key_do(self, keyin):
        q = self.hash_method_list.get()
        if q == "Без хэширования": return keyin
        elif q == "md5": return hashlib.md5(keyin.encode()).hexdigest()
        elif q == "sha1": return hashlib.sha1(keyin.encode()).hexdigest()
        elif q == "sha256": return hashlib.sha256(keyin.encode()).hexdigest()
        elif q == "sha224": return hashlib.sha224(keyin.encode()).hexdigest()        
        elif q == "sha512": return hashlib.sha512(keyin.encode()).hexdigest()
        elif q == "sha3_224": return hashlib.sha3_224(keyin.encode()).hexdigest()
        elif q == "sha3_256": return hashlib.sha3_256(keyin.encode()).hexdigest()
        elif q == "sha3_384": return hashlib.sha3_384(keyin.encode()).hexdigest()
        elif q == "sha3_512": return hashlib.sha3_512(keyin.encode()).hexdigest()
        
        
    def file_choise(self):
        self.file = ''
        self.file = askopenfilename(filetypes = (("All types", ".*"),))
        if self.file != '': self.file_entried['text'] = "✔"

def makewindow():
    root = Tk()
    root.geometry("500x500")
    root.resizable(False,False)
    q = Main_window(root)
    root.mainloop()    


def main():
    makewindow()

if __name__ == '__main__':
    main()