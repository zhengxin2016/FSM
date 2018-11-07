#!/usr/bin/env python3
#from transitions import Machine
from transitions.extensions import GraphMachine as Machine

class Matter:
    pass

model = Matter()

states = ['solid', 'liquid', 'gas', 'plasma']

transitions = [
        {'trigger':'melt', 'source':'solid', 'dest':'liquid'},
        {'trigger':'evaporate', 'source':'liquid', 'dest':'gas'},
        {'trigger':'sublimate', 'source':'solid', 'dest':'gas'},
        {'trigger':'ionize', 'source':'gas', 'dest':'plasma'},
        ]

machine = Machine(model=model, states=states, transitions=transitions, initial='solid')


print(model.state)
model.melt()
print(model.state)
model.trigger('evaporate')
#model.ionize()
print(model.state)


model.get_graph().draw('test.png', prog='dot')
#model.get_graph(show_roi=True).draw('test.png', prog='dot')
