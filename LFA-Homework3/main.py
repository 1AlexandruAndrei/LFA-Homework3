#functie pt lambda inchideri
def lambdainc(states, nfa):
    closure=set(states)
    queue=list(states)
    while queue:
        state=queue.pop(0)
        lambda_transitions=[]
        if state in nfa and '-' in nfa[state]:
            lambda_transitions=nfa[state]['-']

        for next_state in lambda_transitions:
            if next_state not in closure:
                closure.add(next_state)
                queue.append(next_state)
    return sorted(list(closure))

def transformare(nfa, initial_state, alfabet):
    initial_closure=lambdainc([initial_state], nfa)
    dfa=dict()
    states_queue=[initial_closure]
    processed_states=set() #ca sa vad starile pe care le am procesat deja

    while states_queue:
        current_state=states_queue.pop(0)

        if tuple(current_state) in processed_states:
            continue

        processed_states.add(tuple(current_state))
        dfa[tuple(current_state)]={}#in matricea de adiacenta o pun

        for symbol in alfabet:
            next_state=set()

            for nfa_state in current_state:
                if nfa_state in nfa:

                    if symbol in nfa[nfa_state]:
                        transitions=nfa[nfa_state][symbol]
                    else:
                        transitions=[]

                else:
                    transitions=[]

                next_state.update(transitions)

            next_closure=lambdainc(next_state, nfa)

            if tuple(next_closure) not in processed_states:#mai am st de trecut prin ele
                states_queue.append(next_closure)
                
            dfa[tuple(current_state)][symbol]=tuple(next_closure)

    return dfa

def output(dfa, f, final_states):
    with open(f, 'w') as fisier:
        initial_state=next(iter(dfa))#prima din sanga
        fisier.write(f"Stare initiala: {initial_state}\n")
        fisier.write("-----------------------------------------------------------\n")


        final_states_dfa=[]
        for stare in dfa:
            for x in final_states:
                if x in stare:
                    final_states_dfa.append(stare)#adaug daca gasesc vreuna buna
                    break

        fisier.write(f"Stari finale: {','.join(str(stare) for stare in final_states_dfa)}")
        fisier.write("\n")
        fisier.write("-----------------------------------------------------------\n")

        for stare in dfa:
            if stare:
                for symbol in dfa[stare]:
                    next_state = dfa[stare][symbol]
                    fisier.write(f"{stare}----{symbol}---->{next_state}")
                    fisier.write("\n")
                fisier.write("-----------------------------------------------------------\n")

nfa={}
alfabet={}
with open('file.in') as file:
    initial_state=file.readline().strip()
    final_states=file.readline().strip().split()
    alfabet=file.readline().split()
    for l in file:

        linie=l.strip().split(' ')
        current_state, symbol, next_state=linie

        if current_state not in nfa:
            nfa[current_state]={}
        
        if symbol not in nfa[current_state]:
            nfa[current_state][symbol]=[next_state]
        else:
            nfa[current_state][symbol].append(next_state)
dfa=transformare(nfa, initial_state, alfabet)
output(dfa, 'file.out', final_states)
