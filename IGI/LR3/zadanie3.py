def task3():
    num = 0
    text = str(input("Введите строку: "))
    for b in text:
        if(b>='g' and b<='o'):
            num+=1
    if(num!=None):
        print(f"количество символов, лежащих в диапазоне от 'g' до 'o': {num}")
    else:
        print("Не ввели строку или из заданного диапазона нет букв")    