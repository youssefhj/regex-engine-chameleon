class Automaton:
    """
    Automaton is a model of state machine

    Helps in:
        (1) Defining an automaton
        (2) Check if the automaton an epsilon-NFA, NFA or DFA
        (3) Converting epsilon-NFA ---To---> NFA ---To---> DFA
    """
    def __init__(self, alphabet: set = None, init_states: set = None, final_states: set = None, states: set = None, transitions: dict = None) -> None:
        """
        Initialize the state of automaton

        :param alphabet: Symbols knows by the automate
        :param init_states: The starting states
        :param final_states: The final states where machine halts
        :param states: The set of all states (ie Initials + Finals + Others)
        :param transitions: The transition between state (i.e (state_i, symbol, state_j)
        """
        self.alphabet = alphabet
        self.init_states = init_states
        self.final_states = final_states
        self.states = states
        self.transitions = transitions


    def is_epsilon_NFA(self) -> bool:
        """
        Checks the existing of epsilon transition on the given automaton

        :return: True if the automaton is an epsilon-NFA
                 False otherwise
        """
        for _, symbol in self.transitions:
            if symbol == '':
                return True

        return False

    def is_NFA(self) -> bool:
        """
        Checks if there is multiple transition
        with the same symbol from the same source state on the given automaton
        (i.e. (state_i, `symbol`, state_j) and (state_i, `symbol`, state_k))

        :return: True if the automaton is an NFA
                 False otherwise
        """
        if self.is_epsilon_NFA() or len(self.init_states) > 1:
            return True

        for k in self.transitions:
            if len(self.transitions[k]) > 1:
                return True

        return False

    def is_DFA(self) -> bool:
        """
        Checks if the given automaton is deterministic
        (i.e. foreach state there is one transition with symbol_X to other ones)

        :return: True if the automaton is an NFA
                 False otherwise
        """
        return not self.is_NFA()

    def eliminate_epsilon_transition(self) -> None:
        """
        Eliminate all transition with
        epsilon symbol (i.e. delete(state_i, epsilon, state_j))

        :return: None
        """
        states_to_delete = list(filter(lambda symbol: symbol[1] == '', self.transitions))

        for s in states_to_delete:
            del self.transitions[s]

    def epsilon_closure_of_state(self, state: str | int) -> set:
        """
        Takes a certain state then it returns
        all states possible that can be reached from state with epsilon* transition
        (i.e. epsilon* closure)

        :param state: Some state
        :return: Set for all epsilon* transition from state `state`
        :raise: Exception in case state not existing in the automaton definition
        """
        if state not in self.states:
            raise Exception(f'{state} not existing in definition of automaton')

        return self.__go_recursion_epsilon_closure_of_state(state)

    def __go_recursion_epsilon_closure_of_state(self, state: str | int) -> set:
        """
        It's a helper method for `epsilon_closure_of_state` method
        Goes recursion over states from state until it reach a dead ends
        then it returns all states that can be reached with epsilon* transition

        :param state: Some state
        :return: Set for all epsilon* transition from state `state`
        """
        # All states that can be reached from `state` with epsilon* transition (i.e state --epsilon*--> ??)
        all_states = set()
        all_states.add(state)

        if self.transitions.get((state, '')) is not None:
            for s in self.transitions[(state, '')]:
                if state != s:
                    all_states.update(self.epsilon_closure_of_state(s))

        return all_states

    def __set_transitions_for_state(self, target_state: str | int, dependency_state: str | int) -> dict:
        """
        Adding all transition of dependency state to the target state
        (i.e. (dependency_state, symbol_X, state_X) added to target like (target_state, symbol_X, state_X))

        :param target_state: State that need transitions changes
        :param dependency_state: A State that target state depends on
        :return: Old transitions + New transitions for target_state
        """
        # Get all transitions of the dependency state
        dependency_state_transitions = list(filter(lambda state_and_symbol: state_and_symbol[0] == dependency_state, self.transitions))
        other_possible_transitions = {}
        transitions_copy = self.transitions.copy() # Making copy to avoid changing the original transitions for the given automaton

        # Initialization with transitions for target state
        for state, symbol in transitions_copy:
            if state == target_state:
                if (state, symbol) in other_possible_transitions:
                    other_possible_transitions[(state, symbol)].update({(state, symbol): transitions_copy[(state, symbol)]})
                else:
                    other_possible_transitions.update({(state, symbol): transitions_copy[(state, symbol)]})

        # Adding new transitions for target state
        for state, symbol in dependency_state_transitions:
            if (target_state, symbol) in other_possible_transitions:
                other_possible_transitions[(target_state, symbol)].update(self.transitions[(state, symbol)].copy())
            else:
                other_possible_transitions[(target_state, symbol)] = self.transitions[(state, symbol)].copy()

        return other_possible_transitions

    def __get_transitions_of_state(self, state: set) -> dict:
        """
        Get all direct states for the given state

        :param state: Set of states
        :return: Dictionary of transitions with all possible symbol in alphabet
        :raise: Exception if state is a None value
        """
        if state is None:
            raise Exception('Error: None value')

        if len(state) <= 0:
            return {}

        state_transitions = {}
        for symbol in self.alphabet:
            founded_states = set()
            for s in sorted(state):
                if self.transitions.get((s, symbol)) is not None:
                    founded_states.update(self.transitions[(s, symbol)])

                state_transitions[(tuple(sorted(state)), symbol)] = tuple(sorted(founded_states)) if len(founded_states) > 0 else ()

        return state_transitions

    def eNFA_to_NFA(self) -> 'Automaton':
        """
        Convert automaton from epsilon-NFA to NFA

        :return: New Automaton
        """
        if self.is_epsilon_NFA():
            epsilon_closure_of_all_states = {}
            new_transitions = {}

            # Foreach state we need to know all states with epsilon* transition
            for s in self.states:
                epsilon_closure_of_all_states[s] = self.epsilon_closure_of_state(s)

            # Know we should eliminate all epsilon transition
            self.eliminate_epsilon_transition()

            # After we have the epsilon-closure for each state of our Automaton
            # Know we do changes on old Automaton (A) to new Automaton' (A')
            # By changing transitions and final state set if possible
            for state in epsilon_closure_of_all_states:
                for state_state in epsilon_closure_of_all_states[state]:
                    if state_state in self.final_states:
                        self.final_states.add(state)

                    # What are the transition of state state_state
                    # after founding that we simply add it to the transitions of state (i.e (state, ?, state_state))
                    result_transition = self.__set_transitions_for_state(state, state_state)
                    for r_t in result_transition:
                        if r_t in new_transitions:
                            new_transitions[r_t].update(result_transition[r_t])
                        else:
                            new_transitions.update(result_transition)

            if len(new_transitions) > 0:
                self.transitions.clear()
                self.transitions.update(new_transitions)

        return self

    def NFA_to_DFA(self) -> 'Automaton':
        """
        Convert automaton from NFA to DFA

        :return: New Automaton
        """
        if self.is_epsilon_NFA():
            self.eNFA_to_NFA()

        if self.is_NFA():
            new_transitions = {} # This the transitions for the automaton after determinization
            new_states = set() # The new states for the new automaton
            new_final_states = set() # The new final state for the new automaton
            states_already_processed = [] # Track the states that already processed
            states_needs_processing = [self.init_states]
            name_mapper = {} # Help to give new name to state after determinization
            state_number = 0 # This track number of state

            # Algorithm is too simple
            # We loop until the stack of states needs processing is empty
            # If we process some state we put it in the stack of states already processed to keep track
            while len(states_needs_processing) > 0:
                state = states_needs_processing.pop()

                if state in states_already_processed:
                    continue

                result_states =  self.__get_transitions_of_state(state)
                print(result_states)
                if len(result_states) > 0:
                    states_already_processed.append(state)

                    for s in result_states:
                        if s[0] not in name_mapper:
                            new_states.add(state_number)
                            name_mapper[s[0]] = state_number

                            # Checks for new final states
                            for sub_state in s[0]:
                                if sub_state in self.final_states:
                                    new_final_states.add(state_number)

                            state_number += 1

                        if result_states[s] is None or len(result_states[s]) <= 0:
                            continue

                        if result_states[s] not in states_already_processed:
                            states_needs_processing.append(result_states[s])

                        # Here we are sure that the state has transitions to other ones
                        new_transitions.update({s: result_states[s]})

            self.transitions = {}
            self.final_states = new_final_states
            self.states = new_states

            # We simply map each new state with its corresponding number
            # Just to simplify thing, its the same automaton it recognized the same language as previous
            for state, symbol in new_transitions:
                self.transitions[(name_mapper[state], symbol)] = {name_mapper[new_transitions[(state, symbol)]]}

        return self

    def __repr__(self) -> str:
        """
        Helps in debugging

        :return: Formated String
        """
        return f"Automaton(alphabet={self.alphabet}, init_states={self.init_states}, final_states{self.final_states}, states={self.states}, transitions={self.transitions})"