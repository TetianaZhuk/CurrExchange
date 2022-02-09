import json
import requests
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox





#Получение текущих курсов в Приватбанк и 
# размещение полученных данных во временный файл

def request():
    resp = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
    if resp.status_code == 200:
        data=json.loads(resp.text)
        with open("CurExchange/courses.json","w") as file:
            json.dump(data,file)
    else:
        messagebox.showinfo("Ошибка","Сервер не отвечает, попробуйте еще раз немного позже")

# Получение списка всех возможных валют из временного файла
# для заполнения выпадающего списка для валюты покупки и валюты продажи

def getList():
    request()
    with open("CurExchange/courses.json","r") as file:
        data=json.load(file)
    v_list=[]
    for i in range(0,len(data)):
        if (data[i]["ccy"]) not in v_list:
            v_list.append(data[i]["ccy"])
    for i in range(0,len(data)):
        if data[i]["base_ccy"] not in v_list:
            v_list.append(data[i]["base_ccy"])
    return v_list

#__________Определение обменного курса для выбранной валютной пары 
# (поиск совпадающей валютной пары во временном файле,с учетом типа операции)

def getCourse(v_buy, v_sale):
    with open("CurExchange/courses.json","r") as file:
        data=json.load(file)
    for i in range (0,len(data)):
            if data[i]["ccy"]==v_buy and data[i]["base_ccy"]==v_sale:
                course = float(data[i]["sale"])
                print(course)
                return course
            elif data[i]["ccy"]==v_sale and data[i]["base_ccy"]==v_buy:
                course = 1/(float(data[i]["buy"]))
                print(course)
                return course
    else: messagebox.showinfo("Отсутствуют данные", "Конвертация невозможна, выберите другую валюту")   

            
#Получение введенных данных при нажатии кнопки Расчет

def click():
    pass
    global v_buy
    global v_sale
    global sum_buy
    global sum_sale
    v_buy = box_Buy.get()
    v_sale = box_Sale.get()
    sum_buy = float(ent_Buy.get())
    sum_sale = float(ent_Sale.get())
    count(v_buy,v_sale,sum_buy,sum_sale)

#Hfcxtn cevvs
def count(v_buy,v_sale,sum_buy,sum_sale):
    if v_buy =="" or v_sale=="":
        messagebox.showinfo("Ошибка заполнения", "Введите значение валюты покупки и валюты продажи")
    else:
        print ("Валюта покупки:",v_buy,type(v_buy),"\n",
            "Валюта продажи:",v_sale,type(v_sale),"\n",
            "Сумма покупки:",sum_buy,type(sum_buy),"\n",
            "Сумма продажи:",sum_sale,type(sum_sale),"\n")
        if sum_sale == 0 and sum_buy != 0:
            print("Продажа")
            course=getCourse(v_buy,v_sale)
            sum_sale = round(sum_buy*course,2)
            ent_Sale.delete(0,tk.END)
            ent_Sale.insert(0, sum_sale)      
        elif sum_sale != 0 and sum_buy == 0:
            print("Покупка")
            course=getCourse(v_buy,v_sale) 
            sum_buy = round(sum_sale/course,2)
            ent_Buy.delete(0,tk.END)
            ent_Buy.insert(0, sum_buy)     
        else:
            messagebox.showinfo("Ошибка заполнения", "Введите значение одной из сумм, вторая будет рассчитана автоматически")
  
#Обработчики событий:

def callback(event): #изменение полей для выбора валют вызывает обнуление полей для ввода сумм
    print("Выбран новый элемент, суммы обнуляются")
    ent_Buy.delete(0,tk.END)
    ent_Buy.insert(0,0)
    
    ent_Sale.delete(0,tk.END)
    ent_Sale.insert(0,0)

def callback_buy(event): #изменение поля для ввода суммы покупки обнуляет поле для ввода суммы продажи
    print("Обнуляем сумму продажи")
    ent_Sale.delete(0,tk.END)
    ent_Sale.insert(0,0)

def callback_sale(event): #изменение поля для ввода суммы продажи обнуляет поле для ввода суммы покупки
    print("Обнуляем сумму покупки")
    ent_Buy.delete(0,tk.END)
    ent_Buy.insert(0,0)


#ГЛАВНОЕ ОКНО   
        
window = tk.Tk()
window.title('Конвертер валют')


#подписи столбцов и строк виджетов
lb1 = tk.Label(text='ВАЛЮТА')
lb2 = tk.Label(text='CУММА')
lb_Buy = tk.Label(text='КУПИТЬ')
lb_Sale = tk.Label(text='ПРОДАТЬ')

# формируем выпадающий список всех возможных валют
v_list=getList()
print(v_list)

# виджеты для выбора валюты покупки и валюты продажи
buy_txt=tk.StringVar()
sale_txt=tk.StringVar()
box_Buy = ttk.Combobox  (textvariable=buy_txt,
                        values=v_list)
box_Sale = ttk.Combobox (textvariable=sale_txt,
                        values=v_list)

box_Buy.bind("<<ComboboxSelected>>", callback) #если выбирается новая валюта покупки или валюта продажи,
box_Sale.bind("<<ComboboxSelected>>", callback) #обнуляем поля для ввода сумм

# виджеты для суммы покупки и продажи валюты
v_buy = tk.StringVar()
v_sale = tk.StringVar()
sum_buy = tk.DoubleVar()
sum_sale = tk.DoubleVar()

ent_Buy = tk.Entry(textvariable=sum_buy)
ent_Sale = tk.Entry(textvariable=sum_sale)
ent_Buy.bind("<KeyRelease>", callback_buy) #обнуляем сумму продажи при вводе суммы покупки
ent_Sale.bind("<KeyRelease>", callback_sale) #обнуляем сумму покупки при вводе суммы продажи

#кнопка Расчет, запускает обработку введенных данных
btn = tk.Button(text='Расчет', command=click)

#задаем расположение виджетов
lb1.grid(row=0, column=1)
lb2.grid(row=0,column=2)
lb_Buy.grid(row=1, column=0)
box_Buy.grid(row=1,column=1)
ent_Buy.grid(row=1,column=2)
lb_Sale.grid(row=2, column=0)
box_Sale.grid(row=2,column=1)
ent_Sale.grid(row=2,column=2)
btn.grid(row=3,column=1, columnspan=2)


window.mainloop()




