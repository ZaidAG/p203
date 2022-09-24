import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []
questions=[
"1. How many Infinity Stones are there? /n a.3/n b.5/n c.6/n d.10/n",
"2. What is the only food that cannot go bad? /n a.Dark chocolate/n b.Peanut butter/n c.Canned tuna/n d.Honey/n",
"3. Which was René Magritte’s first surrealist painting? /n a.Not to Be Reproduced/n b.Personal Values/n c.The Lovers/n d.The Lost Jockey/n",
"4. What 90s boy band member bought Myspace in 2011? /n a.Nick Lachey/n b.Justin Timberlake/n c.Shawn Stockman/n d.AJ McLean/n",
"5. What is the most visited tourist attraction in the world? /n a.Eiffel Tower/n b.Statue of Liberty/n c.Great Wall of China/n d.Colosseum/n",
"6. What’s the name of Hagrid’s pet spider? /n a.Nigini/n b.Crookshanks/n c.Aragog/n d.Mosag/n",
"7. What’s the heaviest organ in the human body? /n a.Brain/n b.Liver/n c.Skin/n d.Heart/n",
"8. Who made the third most 3-pointers in the Playoffs in NBA history? /n a.Kevin Durant/n b.JJ Reddick/n c.Lebron James/n d.Kyle Korver/n",
"9. Which of these EU countries does not use the euro as its currency? /n a.Poland/n b.Denmark/n c.Sweden/n d.All of the above",
"10. Which US city is the sunniest major city and sees more than 320 sunny days each year? /n a.Phoenix/n  b.Miami/n c.San Francisco/n d.Austin/n",
"11. What type of food holds the world record for being the most stolen around the globe? /n a.Wagyu beef/n b.Cheese/n c.Coffee/n d.Chocolate/n",
"12. What element does the chemical symbol Au stand for? /n a.Silver/n b.Magnesium/n c.Salt/n d.Gold/n",
"13. What is the highest-grossing Broadway show of all time? /n a.The Lion King/n b.Wicked/n c.Kinky Boots/n d.Hamilton/n",
"14. On average, how many seeds are located on the outside of a strawberry? /n a.100/n b.200/n c.400/n d.500/n",
"15. Which fast food restaurant has the largest number of retail locations in the world? /n a.Jack In The Box/n b.Chipotle/n c.Subway/n d.McDonald’s/n",
"16. Where is recognized as the location of the hottest temperature ever recorded on Earth? /n a.Mitribah, Kuwait/n b.Death Valley, California/n c.Yuma, Arizona/n d.Key West, Florida/n",
"17. What is the oldest soft drink in the United States? /n a.Coca Cola/n b.Pepsi/n c.Dr. Pepper/n d.Canada Dry Ginger Ale/n",
"18. What river passes through New Orleans, Louisiana? /n a.Orleans River/n b.Mississippi River/n  c.Atchafalaya River/n d.Colorado River/n"
]
answers=['c','d','d','b','a','c','b','c','d',"a– Phoenix sees more than 320 sunny days each year.","b– It’s estimated that as much as 4% of the cheese produced around the world is stolen.",'d','a','b','c','b','c','b']

print("Server has started...")

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, nickname):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one of a, b, c or d!\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    print(answer)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(": ")[-1].lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
                print(answer)
            else:
                remove(conn)
                remove_nickname(nickname)
        except Exception as e:
            print(str(e))
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print (nickname + " connected!")
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()