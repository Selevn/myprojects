#Steganography prog
#coding=utf8
#тема такая: то что 124 не кодим это кончено хорошо но хуйня полная фикси ибо если случайно 124 вышло - крашится все.
import os
import hashlib
from PIL import Image, ImageDraw

def loading( fwhat, fwhere ):
    #список поддерживаемых расширений
    applied_list = ('.png','.jpg','.bmp','.jpeg')
    
    #размер имени файла + соль
    name_size = 0
    
    #каждый какой пиксель кодировать
    hiding_step = 1
    #Подгружаем файл который скрываем и получаем его данные
    f_what=fwhat  #input('What-file: ') #путь
    f_what_name = os.path.basename(f_what) #имя
    f_what_suf = os.path.splitext(f_what_name)[1] #расширение [0] для имени без расширения
    f_what_size = os.path.getsize(f_what) #размер в байтах
    #print(f_what)
    #print(f_what_name)
    #print(f_what_suf)
    #print(f_what_size)
    name_size = len(f_what_name)+25
    #подгружаем файл в который скрываем и получаем данные
    f_where=fwhere  #input('Where-file: ') #путь
    f_where_name = os.path.basename(f_where) #имя
    f_where_suf = os.path.splitext(f_where_name)[1] #расширение [0] для имени без расширения
    f_where_size = os.path.getsize(f_where) #размер в байтах
    #print(f_where)
    #print(f_where_name)
    #print(f_where_suf)
    #print(f_where_size)
    #проверка формата
    if (f_where_suf == '.JPG'):
        f_where_suf = '.jpg'
    #print(f_where_suf)
    if not (f_where_suf in applied_list) : 
        print('Unsupported format!')
        return False
    #проверка на вмещаемость
    #comress_weight - кол-во кодируемых бит
    if f_where_size//4 < f_what_size+name_size:
        if f_where_size//2 < f_what_size:
            #print('Container is too small for this file')
            return (('Ошибка!','Контейнер очень мал для этого файла! Выберите изображение большего размера.'))
        #elif f_where_size//2 > f_what_size+name_size:
          #  while True:
            #    ans = input('Container is small, but file can be compressed badly. Do you want to continue?(y/n)')
              #  if ans == 'y': 
               #     comress_weight = 4
             #       break
             #   elif ans == 'n':
               #     return False
             #   else:
                 #   print('Unknown symbol, try again(y/n)!!!')
    else:
        #определяем шаг. потом пришьем
        q = f_where_size//4
        if q // (f_what_size+name_size) > 1: hiding_step = q//(f_what_size+name_size) - 1
        if hiding_step>250: hiding_step = 250
        comress_weight = 2
    #открываем файлы
    f_what_body = open(f_what,"rb")
    f_where_body = f_where
    fout_name = f_where
    output_file_body = f_where
    return [f_what_body ,  f_where_body ,  output_file_body ,  f_what_name ,  comress_weight ,  hiding_step ,  f_where_suf]
                

#главная функция которая связывает модули
def main():
    
    while True:
        ans = input('code or decode?(c/d)')
        if ans == 'c':
            while True:
                output_loading = loading()
                if isinstance(output_loading,list):break
            #print('exit!')
            #print(output_loading)
            password = passmaking()
            coding(*output_loading ,  password)
            while True:
                pass
        elif ans == 'd':
            #decoding
            decoding()
            while True:
                pass
        else:
            print('eng pls')
        
        
def includes(list_where,list_what):
    position = 0
    while True:
        returned = False
        again = False
        try:
            pos = list_where.index(list_what[0],position)
        except ValueError:
            returned = True
        if returned: return -1 #end of cycle
        
        add_list = list_where[pos:len(list_what)+pos]
        q = 0
        
        for letter in add_list:
            if not (letter == list_what[q]):
                position = pos+1
                again = True
                break
            else:
                q+=1
        if not again: return pos

def decoding(password_in, file_in):
    print(password_in)
    print(file_in)
    taking_step = True
    password = hashlib.sha512(password_in.encode('utf-8')).hexdigest()
    password = str.encode(password)
    file_place = file_in#input('Your file: ')
    file_place_dir = os.path.dirname(file_place)
    image = Image.open(file_place) #Image.open(input('picture:'))
    draw = ImageDraw.Draw(image)
    width = image.size[0] #Определяем ширину. 
    height = image.size[1]     #Определяем высоту. 	
    pix = image.load()
    pixels_array = []
    for i in range(width):
        for j in range(height):
            #имеем массив из значений rgb каждого пикселя без их индекса
            pixels_array.append(pix[i,j][0])
            pixels_array.append(pix[i,j][1])
            pixels_array.append(pix[i,j][2])
    
    
    first_step = password[0]
    #password[:20] - конец файла!!!
    k = 0
    position_in_password = 0
    hiding_step = 0
    position_to_hide = first_step + hiding_step*k
    
    breaker = False
    #проблема в сдвиге: по магической причине первый(со сдвигом на 6) должен оказываться вконце
    
    #print(pixels_array[first_step + hiding_step*k])
    #print(pixels_array[first_step+1 + hiding_step*k])
    #print(pixels_array[first_step+2 + hiding_step*k])
    #print(pixels_array[first_step+3 + hiding_step*k])
    
    a = (pixels_array[first_step + hiding_step*k]&3) << 6
    a = a + ((pixels_array[first_step+1 + hiding_step*k]&3) << 4)
    a = a + ((pixels_array[first_step+2 + hiding_step*k]&3) << 2)
    a = a + (pixels_array[first_step+3 + hiding_step*k]&3)
    hiding_step = a^password[position_in_password]
    k+=1
    #вытягиваем имя и кодировку
    info = []
    position_in_password+=1
    first_step+=4
    while True:
        try:
            
            if position_in_password==len(password): position_in_password = 0
            position_where_hide = first_step + hiding_step*k
            a = (pixels_array[first_step + hiding_step*k]&3) << 6
            k+=1
            position_where_hide = first_step + hiding_step*k
            a = a + ((pixels_array[first_step + hiding_step*k]&3) << 4)
            k+=1
            position_where_hide = first_step + hiding_step*k
            a = a + ((pixels_array[first_step + hiding_step*k]&3) << 2)
            k+=1
            position_where_hide = first_step + hiding_step*k
            a = a + (pixels_array[first_step + hiding_step*k]&3)
            k+=1
            position_where_hide = first_step + hiding_step*k
            
            a = a ^ password[position_in_password]
            
            
            if not (a == 124): 
                info.append(a)
                position_in_password+=1
            if (a == 124) and not (breaker):
                if taking_step == True:
                    taking_step = False
                    #получили компрессию
                    if info[0] == 50:
                        comprassion = 2
                    elif info[0] == 52: comprassion = 4
                    else: comprassion = 2
                    info.clear()
                else:
                    #получили имя файла
                    file_name = ''
                    for letter in info:
                        file_name+=chr(letter)
                    info.clear()
                    #print(file_name)
                    breaker = True
                position_in_password+=1
        except IndexError:
            #print('shit happends')
            #print(info)
            break
        #вытянули имя
    position_of_EOF = includes(info,password[:20])
    #print(position_of_EOF)
    if position_of_EOF == -1: 
        print('fail!')
        return (['Ошибка!',"Файл не найден! Возможно неверно введен пароль!"])
    name_of_out = file_place_dir+"\\"+file_name
    fout = open(name_of_out,'wb')
    fout.write(bytearray(info[:position_of_EOF]))
    #for i in info[:position_of_EOF]:
        #fout.write(bytes([i])) #копирует только англ символы
        #fout.write(i.decode('utf8'))
        #fout.write(chr(i))
    fout.close()
    return("Файл {} успешно извлечен!".format(file_name))
    #print('success!')
        
        
        
    
    
    
    
#создание пароля
def passmaking(passwd1):
    while True:
        passwd = passwd1#input('Enter your password:')
        if len(passwd)>4: break
        else: return(('Ошибка!','Пароль должен быть длиннее 4х символов!'))
    return hashlib.sha512(passwd.encode('utf-8')).hexdigest()

def coding(f_what_body ,  f_where_body ,  output_file_body ,  f_what_name ,  comress_weight ,  hiding_step ,  f_where_suf,  password):
    password = str.encode(password)
    pixels_array = []
    file_array = []
    string_with_info = str(comress_weight)+'|'+f_what_name+'|'
    string_with_info = string_with_info.encode('utf8')
    #строка string_with_info: (шаг\)компрессия\имя\
    #124 - код символа |
    file_array.append(hiding_step)
    for letter in string_with_info:
        file_array.append(letter)
        #print(chr(letter))
    for line in f_what_body:
        for letter in line:
            file_array.append(letter)
            #
    for letter in password[:20]:
        file_array.append(letter)
            #print(chr(letter))
    #шифруем входной файл
    #!!!ПОВТОРИТЬ ЭТУ ЧАСТЬ КОДА ДЛЯ ДЕКОДИРОВАНИЯ!!!!!
    position = 0
    #print(file_array)
    
    for i in range(len(file_array)):
        file_array[i]=file_array[i]^password[position]
        position+=1
        if position==len(password): position = 0
    #print(file_array)
    
        
    image = Image.open(f_where_body) #Image.open(input('picture:'))
    draw = ImageDraw.Draw(image) #Создаем инструмент для рисования. 
    width = image.size[0] #Определяем ширину. 
    height = image.size[1]     #Определяем высоту. 	
    pix = image.load()
    
    position = 0 #с каким элементом хэша сравнивать
    for i in range(width):
        for j in range(height):
            #имеем массив из значений rgb каждого пикселя без их индекса
            pixels_array.append(pix[i,j][0])
            pixels_array.append(pix[i,j][1])
            pixels_array.append(pix[i,j][2])
    #file_array - массив файла
    #pixels_array - массив контейнера
    
    #сделать так чтобы в первые 4-2 pixels_array записывались первое значение из file_array
    #записывать эти пиксели или сразу в матрицу или в отдельный массив
    #злоупотреблять << и >>   и использовать ^(вроде это).
    #из прошлого опыта лучше использовать & с нужным кол-вом байт(что-то & 00000011/11111100)
    #3 = 00000011
    #12 = 00001100
    #48 = 00110000
    #192 = 11000000
    #240 = 11110000
    #15 = 00001111
   
    #comress_weight
    add_array = []
    
        #compres = 2
    first_step = password[0] #для усложнения взлома - начало отсчета с первого символа пароля
    out_position = 0
    position_counter = 0
    is_first_step = True
    if comress_weight==2:
        for every_symbol in file_array:
            #берем последовательнo 4 пары бит и сдвигаем их к младшим
            add_array.append((every_symbol&192)>>6)
            add_array.append((every_symbol&48)>>4)
            add_array.append((every_symbol&12)>>2)
            add_array.append(every_symbol&3)
            if is_first_step:
                for i in range(len(add_array)):
                    position_to_hide = first_step+position_counter
                    pixels_array[position_to_hide] = pixels_array[position_to_hide] & 252
                    pixels_array[position_to_hide] = pixels_array[position_to_hide] | add_array[i]
                    written = pixels_array[position_to_hide]
                    position_counter+=1
                add_array.clear()
                is_first_step = False
                k = 1
                first_step+=4
            else:
                for i in range(len(add_array)):
                    position_to_hide = first_step+hiding_step*k
                    pixels_array[position_to_hide] = pixels_array[position_to_hide] & 252
                    pixels_array[position_to_hide] = pixels_array[position_to_hide] | add_array[i]
                    written = pixels_array[position_to_hide]
                    k+=1
                add_array.clear()
                
    #print(pixels_array[51])
    #print(pixels_array[52])
    #print(pixels_array[53])
    #print(pixels_array[54])
    
    q=0
    for i in range(width):
        for j in range(height):
            #имеем массив из значений rgb каждого пикселя без их индекса
            draw.point((i, j), (pixels_array[q],pixels_array[q+1],pixels_array[q+2]))
            q+=3
    f_what_body.close()
    os.remove(output_file_body)
    print(output_file_body)
    if f_where_suf[1:]== 'jpg':
        #suffix = 'jpeg'
        suffix = 'png'
        name = os.path.splitext(os.path.basename(output_file_body))[0]
        output_file_body = os.path.dirname(output_file_body)+'//'+name+'.png' #проработать имя файла
        
        print(output_file_body)
    else:
        suffix = f_where_suf[1:]
    image.save(output_file_body, suffix)
    #print('file saved!')
    #print(hiding_step)
    return True
            
            
    
    
    
if __name__ == '__main__': main()