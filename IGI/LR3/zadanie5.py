def task5():
    p_list=[]
    while(True):
        p = input("Введите вещественное число(q для выхода)")
        if(p=="q"):
            break
        try:
            num = float(p)    
            p_list.append(num)
        except:
            print("неправильный ввод")
    min_num = float("inf")
    first_pos,last_pos = -1,0
    for i,n in enumerate(p_list):
        if(n > 0):
            if(n<min_num):
                min_num = n
            if(first_pos==-1):
                first_pos=i
            last_pos = i        
    if(first_pos==last_pos):
        print(f"Введено только одно положительное число: {min_num}")
        return
    if(first_pos==-1):
        print("Не ввели положительные числа")
        return
    i = first_pos
    summa =0
    while(i<last_pos):
        summa += p_list[i]
        i+=1
    print(f"минимальное число: {min_num}")
    print(f"сумма чисел от первого положительного до последнего: {summa}")
    for n in p_list:
        print(n)          