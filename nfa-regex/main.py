import json


def get_transition(d, start, end):
    if d.get(start):
        if d[start].get(end):
            value = ''
            for edge in d[start][end]:
                value += edge + '|'
            return value[:-1]
    return ''


def paranthesis(expr):
    aux = 0
    for i in range(len(expr)):
        if expr[i] == '(':
            aux += 1
        elif expr[i] == ')':
            aux -= 1
        elif expr[i] == '|' and aux == 0:
            return '(' + expr + ')'
    return expr


def star(expr):
    if expr == '' or expr == '$':
        return ''
    if len(expr) == 1:
        return expr + '*'
    return '(' + expr + ')*'


data = []
f = open("input.json", "r")
data = json.load(f)
states = data['states']

transition = {}
"""
Pas 1: a). Verificam daca starea de start are in-deg = 0, iar, in caz contrar, mai adaugam o stare care sa devina stare 
            initiala cu o lambda tranzitie spre vechea stare initiala 
       b). Adaugam o noua stare finala cu lambda-tranzitii de la fiecare stare finala pre-existenta
            (daca unica stare finala care exista nu are out-deg = 0)
       c). Inlocuim muchiile multiple
"""

states.append(0)        # stare de start artificiala
states.append(-1)       # stare de final artificiala
for first in states:
    transition[first] = {}
    for second in states:
        transition[first][second] = get_transition(data["transitions"], first, second)

transition[0][data["start"]] = '$'

for end_state in data["final"]:
    transition[end_state][-1] = '$'


"""
Pas 2: Alegem, pe rand, stari intermediare (diferite de cea initiala si cea finala) pe care sa le eliminam. 
        Fie aceste stari R.
            a). Daca R nu are muchie catre ea insasi, concatenam muchiile care intra in R cu cele care ies din R
            b). Daca R are o muchie catre ea insasi, concatenam muchiile si stelam muchia de la R la R
            c). Daca pasii anteriori conduc la mai multe muchii intre doua stari A si B, le inlocuim cu 
                concatenarea muchiilor
Pas 3: Repetam pasul 2 pana ramanem doar cu doua stari (cea initiala si cea finala) 
"""

for i in range(len(states)-2):
    state = states[i]
    for first in states[i+1:]:
        if transition[first][state] == '':          # tranzitii care ajung in starea curenta
            continue
        for second in states[i+1:]:
            if transition[state][second] == '':     # tranzitii care pleaca din starea curenta
                continue
            old = paranthesis(transition[first][second])
            start = paranthesis(transition[first][state])
            middle = star(transition[state][state])
            final = paranthesis(transition[state][second])
            aux = ''
            if old != '':
                aux = old + '|'
            aux += start
            aux += middle
            aux += final
            aux = aux.replace('$', '')
            transition[first][second] = aux
print("Expresia regulata corespunzatoare este: ")
print(transition[0][-1])

""" Inputul va fi de forma:
{
  "states": ["q1", "q2", "q3"],
  "start": "q1",
  "final": ["q3"],
  "transitions":
  {
    "q1":
    {
        "q2": ["a"],
        "q3": ["b"]
    },
    "q2":
    {
        "q2": ["b"],
        "q3": ["a"]
    },
    "q3":
    {
      "q3": ["a", "b"]
    }
    (etc)
  }
}"""
