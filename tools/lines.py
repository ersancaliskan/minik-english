#!/usr/bin/env python3
"""Lists every sentence Minik English speaks, for pre-recorded voice files.

Run: python3 tools/lines.py  -> writes audio/lines.json
Keep this in step with index.html when topics or sentences change.
Sentences that contain the child's name are left to the device voice.
"""
import json, os, re

NW = ['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve',
      'thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty']
COLORS = ['red','blue','yellow','green','orange','purple','pink','brown','black','white']
WEATHER = [('sunny',"It's sunny!"),('rainy',"It's rainy!"),('cloudy',"It's cloudy!"),('snowy',"It's snowy!"),
           ('windy',"It's windy!"),('stormy',"It's stormy!"),('foggy',"It's foggy!"),('hot',"It's hot!"),
           ('cold',"It's cold!"),('rainbow',"Look, a rainbow!")]
BODY = ['eyes','nose','mouth','ear','hand','finger','arm','leg','foot','teeth','tongue','head','face','neck','body']
SHOWME = ['eyes','nose','mouth','ear','hand','finger','arm','leg','foot','head','face','neck','body']
ANIMALS = [('cat','Meow! Meow!'),('dog','Woof! Woof!'),('rabbit',''),('cow','Moo! Moooo!'),('pig','Oink! Oink!'),
           ('lion','Roar!'),('elephant',''),('sheep','Baa! Baa!'),('zebra',''),('giraffe',''),
           ('monkey','Ooh ooh! Aah aah!'),('bear','Grrr! Grrr!'),('bird','Tweet tweet!'),('duck','Quack! Quack!'),('fish','')]
OBJ = {'home':['house','door','window','wall','table','chair','sofa','bed','lamp','clock'],
       'food':['plate','fork','spoon','cup','milk','water','bread','egg','pasta','cake'],
       'school':['bag','book','notebook','pencil','crayon','eraser','ruler','scissors'],
       'play':['bus','car','bicycle','ball','kite','doll','teddy','shoes']}
EMOS = ['happy','sad','angry','scared','surprised','sleepy','excited','bored','shy','silly']
SHAPES = ['star','heart','ball','house','fish']
DAYS = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

cap1 = lambda s: s[:1].upper() + s[1:]
def short(k):
    if k in ['pasta','milk','water','bread','shoes','scissors']: return cap1(k)+'!'
    return ('An ' if re.match('[aeiou]', k) else 'A ') + k + '!'
def obj_phrase(w):
    if w in ['shoes','scissors']: return "They're "+w+"!"
    if w in ['pasta','milk','water','bread']: return "It's "+w+"!"
    return ("It's an " if re.match('[aeiou]', w) else "It's a ") + w + '!'

L = []
add = lambda *xs: L.extend(xs)

# ---- topics: items and the practice sentences built from them
topics = {}
topics['numbers'] = [dict(say=NW[n]) for n in range(1, 21)]
topics['colors'] = [dict(say=c, color=True) for c in COLORS]
topics['weather'] = [dict(say=w, phrase=p) for w, p in WEATHER]
topics['animals'] = [dict(say=w, phrase=("It's an " if w == 'elephant' else "It's a ")+w+'!', sound=s) for w, s in ANIMALS]
topics['objects'] = [dict(say=w, phrase=obj_phrase(w)) for g in OBJ.values() for w in g]
topics['emotions'] = [dict(say=w, phrase="I'm "+w+"!") for w in EMOS]
topics['body'] = [dict(say=w, phrase='My '+w) for w in BODY]

add(*NW)          # counting / basket / sequences ("one, two, hmm, four" is played word by word)
add('hmm', 'How many?')
for t, items in topics.items():
    for it in items:
        s = it['say']
        add(s, it.get('phrase') or s, s+'!', s+'?', 'Yes! '+s)
        add(('Pop the '+s+' balloon!') if it.get('color') else ('Pop the '+s+'!'))
        if t != 'numbers': add('Find all: '+s+'!')
        if t == 'numbers' and NW.index(s) <= 12: add('Put '+s+' in the basket!')
        if t == 'colors' and s != 'white':
            for sn in SHAPES: add('Paint the '+sn+' '+s+'!', s+' '+sn+'!')
        if it.get('sound'):
            add(it['sound'], 'The '+s+' says '+it['sound'].split('!')[0].lower()+'!')
        if t == 'emotions':
            add("Make "+("an " if re.match('[aeiou]', s) else "a ")+s+" face! Say: I'm "+s+"!")
        if t == 'body' and s in SHOWME:
            add('Touch the '+s+'!', 'Yes! '+s+'!')

# ---- general
add("Hello! Let's play!", 'What did you learn?', 'The end! Great job!', 'Great job!',
    "Hello! I'm Angel. One, two, three! Let's play!")

# ---- story intros
add("Hi! I'm Angel. Today is my birthday!", "Let's count together!", "Yay! Let's play!")
add("Oh no! Where are the colors?", *[cap1(c)+'!' for c in COLORS], "Wow! Look, a rainbow!", "Let's play with colors!")
add("Good morning! What's the weather like today?", "It's sunny!", "It's cloudy.", "It's rainy! Drip, drop!",
    "It's windy! Whoosh!", "It's snowy! Brrr, it's cold!", "Look, a rainbow!", "Let's play!")
add("I'm going to the zoo!", "A lion! Roar!", "An elephant!", "A giraffe!", "A zebra!", "A monkey! Ooh ooh!", "A bear! Grrr!",
    "Now, the farm!", "A cow! Moo!", "A pig! Oink!", "A sheep! Baa!", "A dog! Woof!", "A cat! Meow!", "A rabbit!",
    "A duck! Quack!", "A fish!", "A bird! Tweet!", "I love animals! Let's play!")
add("This is my house!", "A door. Come in!", "A clock! Tick tock!", "And my bed!",
    "I'm hungry!", "And a cake! Yummy!", "Time for school! Let's get ready.", "My bag!", "I'm ready! Let's play!",
    "A bus! Let's go to the park!", "A car! Beep beep!", "My shoes!", "What a fun day! Let's play!", "Look at all my things!")
for g in OBJ.values():
    for k in g: add(short(k))
add('Yaaawn...', 'Good morning!', 'I wash my face!', 'I brush my teeth!', 'Exercise time!', 'Bye-bye!',
    'Hands up!', 'Hands down!', 'Right hand up!', 'Left hand up!', 'Head up!', 'Head down!', 'Foot up!', 'Foot down!',
    'Smell with my nose! Sniff, sniff!', 'Show my tongue!', 'Open my eyes!', 'Close my eyes!', 'Touch my ears!')

# ---- Talk with Angel (questions and answers without the child's name)
add("Hi! I'm Angel. What's your name?", "How are you today?", "How old are you?", "What do you like to eat?",
    "I'm happy to hear that! Me too!", "Oh no! Here is a big hug. Let's play and be happy!", "Sleepy? Let's wake up and play!",
    "Take a deep breath. In... and out. Now let's play!", "Don't worry, I'm here with you!", "Yay! I'm excited too!",
    "Thank you for telling me!", "Hmm, how old? Show me with your fingers!", "What day is it today?",
    "How is the weather today?", "Hmm! Is it sunny or rainy?", "It is hot! Drink some water!",
    "Brrr! It is cold! Wear your coat!", "What is your favorite color?", "That's a nice color!", "Look! What color is it?",
    "How many fingers do you have? Count them!", "Yes! Ten fingers! Well done!",
    "Let's count together: one, two, three, four, five, six, seven, eight, nine, ten! Ten fingers!",
    "Let's count: one, two, three, four, five, six, seven, eight, nine, ten!",
    "Can you count to five? Let's go!", "Wow! Great counting!", "Good try! One, two, three, four, five!",
    "How many eyes do you have?", "Yes! Two eyes! Blink, blink!", "Two! You have two eyes!",
    "What is your favorite animal?", "What a nice animal!", "Yummy! Fruit and vegetables make you strong!",
    "What is in your school bag?", "Books and pencils! Ready for school!",
    "How do you go to school? By car, by bus, or on foot?", "By car! Beep beep!",
    "By bus! The wheels on the bus go round and round!", "On foot! Walking is great!", "By bike! Cool!",
    "Thank you! Let's play!", "Say yes or no!", "I didn't hear you. Say it again!", "That's okay! Let's play!")
add("Nice to meet you!")  # name lines play without the name
for n in range(1, 21):
    add("Wow! You are "+NW[n]+"! "+("You are so big!" if n >= 5 else "So cute!"))
for d in DAYS:
    add("Yes! Today is "+d+"! Well done!", "Good try! Today is "+d+".", "Today is "+d+"!")
for w in ['sunny','rainy','cloudy','snowy','windy','stormy','foggy']:
    add("It is "+w+" today! Thank you!")
for c in COLORS:
    add(cap1(c)+"! I love "+c+" too!")
    if c != 'white': add("Yes! It's "+c+"! Great job!", "It's "+c+"! Say it with me: "+c+"!")
for p in ['nose','head','mouth','ears','eyes']:
    pl = p.endswith('s')
    add(("Where are your " if pl else "Where is your ")+p+"? Touch "+("them" if pl else "it")+" and say: "+("they are here!" if pl else "it is here!"),
        "Yes! Your "+p+(" are" if pl else " is")+" there! Great!", "Touch your "+p+("! They are here!" if pl else "! It is here!"))
for w, snd in ANIMALS:
    add(("An " if re.match('[aeiou]', w) else "A ")+w+"! "+(snd+' ' if snd else '')+"I like "+(w if w in ['sheep','fish'] else w+'s')+" too!")
    if snd: add("What does the "+w+" say?", "Yes! The "+w+" says "+snd, "The "+w+" says "+snd)
for s in ['pasta','bread','eggs','cake','apples','bananas','milk','pizza','chocolate','ice cream']:
    add("Yummy! I like "+s+" too!")
for w in OBJ['school']:
    add(short(w)+" Great! You are ready for school!")
for q, a, b in [("Do you like ice cream?","Me too! Yummy!","Okay! More for me!"),
                ("Is the sky green?","Hmm, really? The sky is blue!","Right! The sky is blue!"),
                ("Do you like cats?","Me too! Meow!","Okay! Maybe dogs?"),
                ("Is a banana yellow?","Yes! Bananas are yellow!","Hmm, bananas are yellow!"),
                ("Can a fish fly?","Haha! No, fish swim!","Right! Fish swim!")]:
    add(q, a, b)

def key(t):  # must match normKey() in index.html
    return re.sub(r'\s+', ' ', t.strip().lower().replace('’', "'"))

seen, out = set(), []
for t in L:
    k = key(t)
    if k and k not in seen:
        seen.add(k); out.append(t)

os.makedirs('audio', exist_ok=True)
json.dump(out, open('audio/lines.json', 'w'), ensure_ascii=False, indent=0)
print(len(out), 'lines,', sum(len(t) for t in out), 'characters')
