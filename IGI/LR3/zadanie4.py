def task4():
    num_space=0
    text="So she was considering in her own mind, as well as she could," \
    " for the hot day made her feel very sleepy and stupid," \
    " whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies," \
    " when suddenly a White Rabbit with pink eyes ran close by her"
    for t in text:
        if(t ==" "):
            num_space+=1
    num_words = (num_space)
    print(f"слов ограниченных пробелами: {num_words}")
    num_letter={}
    for b in text.lower():
        if(b>="a" and b<="z"):
            num_letter[ord(b) - 97] = num_letter.get(ord(b) - 97, 0) + 1
    i=0        
    letters={}
    while(i<26):
        letters[i]=chr(i+97)
        i+=1
    for n in letters:
        print(f"{letters[n]}: {num_letter.get(n,0)}")
    phrases = {}
    copy = ""
    i=0
    for p in text.lower():
        if(p!=","):
            copy+=p
        if(copy==" "):
            copy=""
        if(p==","):
            phrases[i] = copy
            i+=1
            copy="" 
    phrases[i] = copy        
    for n in sorted(phrases.values()):
        print(f"{n}\n")