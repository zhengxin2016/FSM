#!/usr/bin/env python3
#from transitions import Machine
from transitions.extensions import GraphMachine as Machine

class Matter:
    pass

model = Matter()

class FiniteStateMachine:
    '''
    states
    start_state
    end_states
    transitions
    transitions_func
    model
    machine
    '''
    def __init__(self, start='start', end=['end']):
        self.start_state = start
        self.current_state = self.start_state
        self.end_states = end
        self.handlers = transitions_func

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
                trigger = self.handlers[self.current_state](word)
                model.trigger(trigger)
                self.current_state = model.state
                words = words[1:]
        if not words and self.current_state in self.end_states:
            return self.current_state
        else:
            return None

states = ['start', 'prefix', 'entity', 'other', 'end']
end_states = ['other', 'end']
transitions = [
        {'trigger':'prefix_pass', 'source':'start', 'dest':'prefix'},
        {'trigger':'entity_pass', 'source':'prefix', 'dest':'entity'},
        {'trigger':'suffix_pass', 'source':'entity', 'dest':'end'},
        {'trigger':'prefix_fail', 'source':'start', 'dest':'other'},
        {'trigger':'entity_fail', 'source':'prefix', 'dest':'other'},
        {'trigger':'suffix_fail', 'source':'entity', 'dest':'other'},
        ]

machine = Machine(model=model, states=states, transitions=transitions, initial='start')

def start_transitions(word):
    '''
    {prefix_pass, prefix_fail}
    '''
    if not word:
        return 'prefix_pass'
    elif word['ner'] == 'other' and word['token'] in ['', '你知道']:
        return 'prefix_pass'
    else:
        return 'prefix_fail'

def prefix_transitions(word):
    '''
    {entity_pass, entity_fail}
    '''
    if not word:
        return 'entity_fail'
    elif word['ner'] == 'entity':
        return 'entity_pass'
    else:
        return 'entity_fail'

def entity_transitions(word):
    '''
    {suffix_pass, suffix_fail}
    '''
    if not word:
        return 'suffix_pass'
    elif word['ner'] == 'other' and word['token'] in ['', '吗']:
        return 'suffix_pass'
    else:
        return 'suffix_fail'

transitions_func = {
        'start':start_transitions,
        'prefix':prefix_transitions,
        'entity':entity_transitions,
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


