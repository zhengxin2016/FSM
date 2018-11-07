#!/usr/bin/env python3
#from transitions import Machine
from transitions.extensions import GraphMachine as Machine

class Matter:
    pass

model = Matter()

'''
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
'''

########################################################################################

class FiniteStateMachine:
    def __init__(self, start='start', end=['end']):
        self.start_state = start
        self.current_state = self.start_state
        self.end_states = end
        self.handlers = self.get_handlers()

    def get_handlers(self):
        handlers = {}
        for x in transitions:
            if x['source'] in handlers:
                handlers[x['source']].append(x['trigger'])
            else:
                handlers[x['source']] = [x['trigger']]
        return handlers

    def _reset_machine(self):
        self.current_state = self.start_state
        machine.set_state(self.start_state)

    def run(self, words):
        ##############
        if len(words) == 0:
            return None
        if words[0]['ner'] != 'other':
            words = [{'token':'', 'ner':'other'}] + words
        if words[-1]['ner'] != 'other':
            words = words + [{'token':'', 'ner':'other'}]
        ##############
        self._reset_machine()
        while words:
            word = words[0] if len(words) > 0 else {}
            if self.current_state in self.end_states:
                break
            else:
                for handler in self.handlers[self.current_state]:
                    if transitions_func[handler](word):
                        model.trigger(handler)
                        self.current_state = model.state
                        words = words[1:]
                        break
        if not words and self.current_state in self.end_states:
            return self.current_state
        else:
            return None

states = ['start', 'prefix', 'entity', 'other', 'end']
transitions = [
        {'trigger':'prefix_pass', 'source':'start', 'dest':'prefix'},
        {'trigger':'entity_pass', 'source':'prefix', 'dest':'entity'},
        {'trigger':'suffix_pass', 'source':'entity', 'dest':'end'},
        {'trigger':'prefix_fail', 'source':'start', 'dest':'other'},
        {'trigger':'entity_fail', 'source':'prefix', 'dest':'other'},
        {'trigger':'suffix_fail', 'source':'entity', 'dest':'other'},
        ]

machine = Machine(model=model, states=states, transitions=transitions, initial='start')

def prefix_pass(word):
    if not word:
        return True
    elif word['ner'] == 'other' and word['token'] in ['', '你知道']:
        return True
    else:
        return False

def prefix_fail(word):
    if prefix_pass(word):
        return False
    return True

def entity_pass(word):
    if not word:
        return False
    elif word['ner'] == 'entity':
        return True
    else:
        return False

def entity_fail(word):
    if entity_pass(word):
        return False
    return True

def suffix_pass(word):
    if not word:
        return True
    elif word['ner'] == 'other' and word['token'] in ['', '吗']:
        return True
    else:
        return False

def suffix_fail(word):
    if suffix_pass(word):
        return False
    return True

transitions_func = {
        'prefix_pass':prefix_pass,
        'prefix_fail':prefix_fail,
        'entity_pass':entity_pass,
        'entity_fail':entity_fail,
        'suffix_pass':suffix_pass,
        'suffix_fail':suffix_fail,
        }

fsm = FiniteStateMachine(end=['end', 'other'])
data = [
        [],#error
        [{'token':'hello', 'ner':'other'}],#error
        [{'token':'你知道', 'ner':'other'}],#error
        [{'token':'你知道', 'ner':'other'}, {'token':'吗', 'ner':'other'}],#error
        [{'token':'你知道', 'ner':'other'}, {'token':'苏州','ner':'entity'},{'token':'吗', 'ner':'other'},{'token':'?','ner':'other'}],#error
        [{'token':'苏州', 'ner':'entity'}],#ok
        [{'token':'你知道', 'ner':'other'}, {'token':'苏州', 'ner':'entity'}],#ok
        [{'token':'苏州', 'ner':'entity'},{'token':'吗', 'ner':'other'}],#ok
        [{'token':'你知道', 'ner':'other'}, {'token':'苏州','ner':'entity'},{'token':'吗', 'ner':'other'}],#ok
        ]
for words in data:
    ret = fsm.run(words)
    if ret == 'end':
        print('ok')
    else:
        print('error')
model.get_graph().draw('graph.png', prog='dot')


