from types import SimpleNamespace
 
FiniteAutomation = SimpleNamespace
Transition = SimpleNamespace
 
 
def automation_from_expression(expression: str) -> FiniteAutomation:
    next_state_number = 0  # counter for number of all states
    stack_of_automation = []  # stack for reverse polish notation
    for symbol in expression:
        if symbol == " " or symbol == "\n":
            continue
        elif symbol == "1":  # empty-epsilon
            empty_automation = FiniteAutomation()
            empty_automation.states = [next_state_number]  # one state
            empty_automation.start = next_state_number
            empty_automation.finish = next_state_number
            empty_automation.transitions = []
            next_state_number += 1
            stack_of_automation.append(empty_automation)  # add on stack
        elif symbol == '.':  # concat
            right_expr = stack_of_automation.pop()
            left_expr = stack_of_automation.pop()
            concat_automation = FiniteAutomation()
            concat_automation.states = left_expr.states
            concat_automation.states += right_expr.states
            concat_automation.start = left_expr.start
            concat_automation.finish = right_expr.finish
            concat_automation.transitions = left_expr.transitions
            concat_automation.transitions += right_expr.transitions
            way = Transition(
                from_=left_expr.finish,
                to_=right_expr.start,
                by=''
            )
            concat_automation.transitions.append(way)  # add bridge from left.finish to right.start by epsilon
            stack_of_automation.append(concat_automation)
        elif symbol == '+':
            right_expr = stack_of_automation.pop()
            left_expr = stack_of_automation.pop()
            sum_automation = FiniteAutomation()
            sum_automation.states = left_expr.states
            sum_automation.states += right_expr.states
            sum_automation.states.append(next_state_number)
            sum_automation.states.append(next_state_number + 1)
            sum_automation.start = next_state_number  # new start
            sum_automation.finish = next_state_number + 1  # new finish
            sum_automation.transitions = left_expr.transitions
            sum_automation.transitions += right_expr.transitions
            from_start_to_left = Transition(
                from_=next_state_number,
                to_=left_expr.start,
                by=''
            )
            sum_automation.transitions.append(from_start_to_left)  # start -> left.start
            from_start_to_right = Transition(
                from_=next_state_number,
                to_=right_expr.start,
                by=''
            )
            sum_automation.transitions.append(from_start_to_right)  # start -> right.start
            from_left_to_end = Transition(
                from_=left_expr.finish,
                to_=next_state_number + 1,
                by=''
            )
            sum_automation.transitions.append(from_left_to_end)  # left.finish -> finish
            from_right_to_end = Transition(
                from_=right_expr.finish,
                to_=next_state_number + 1,
                by=''
            )
            sum_automation.transitions.append(from_right_to_end)  # right.finish -> finish
            stack_of_automation.append(sum_automation)
            next_state_number += 2  # update counter
        elif symbol == "*":
            edit_automation = stack_of_automation.pop()
            if edit_automation.start == edit_automation.finish:  # check is it stared before (ex. 1*, (a*)* )
                stack_of_automation.append(edit_automation)
                continue
            finish_to_start_edge = Transition(
                from_=edit_automation.finish,
                to_=edit_automation.start,
                by=''
            )
            edit_automation.transitions.append(finish_to_start_edge)  # finish -> start
            edit_automation.finish = edit_automation.start  # finish = start
            stack_of_automation.append(edit_automation)
        else:
            base_automation = FiniteAutomation()
            base_automation.states = [next_state_number, next_state_number + 1]  # 2 states
            base_automation.start = next_state_number
            base_automation.finish = next_state_number + 1
            edge = Transition(
                from_=next_state_number,
                to_=next_state_number + 1,
                by=symbol
            )
            base_automation.transitions = [edge]  # 1 edge: start -> finish by letter
            next_state_number += 2  # update counter
            stack_of_automation.append(base_automation)
    return stack_of_automation.pop()
 
 
def remove_empty_transitions(automation: FiniteAutomation) -> FiniteAutomation:
    new_automation = FiniteAutomation()
    new_automation.transitions = []
    one_letter_transitions = []
 
    def dfs_for_one_letter_transitions(start_state, cur_state):
        for edge in automation.transitions:
            if edge.from_ == cur_state:
                if edge.by != '':  # we found an nonempty edge from start_state to edge.to_
                    new_transmission = Transition(
                        from_=start_state,
                        to_=edge.to_,
                        by=edge.by
                    )
                    one_letter_transitions.append(new_transmission)
                else:  # continue recursion
                    dfs_for_one_letter_transitions(start_state, edge.to_)
 
    for state in automation.states:
        dfs_for_one_letter_transitions(state, state)
 
    new_automation.start = automation.start
    new_automation.states = []
 
    def dfs_for_states(vertex):  # find all reachable states for state vertex
        if vertex in new_automation.states:
            return
        new_automation.states.append(vertex)
        for edge in one_letter_transitions:
            if edge.from_ == vertex:
                dfs_for_states(edge.to_)
 
    dfs_for_states(new_automation.start)  # all reachable states for start
    for transition in one_letter_transitions:  # remove extra copies
        if transition.from_ in new_automation.states:
            new_automation.transitions.append(transition)
 
    def path_to_finish_by_empty_transitions(vertex):  # try to find empty path from vertex to finish
        if vertex == automation.finish:
            return True
        for edge in automation.transitions:
            if edge.from_ == vertex and edge.by == '':
                if path_to_finish_by_empty_transitions(edge.to_):
                    return True
 
        return False
 
    new_automation.finishes = []
    for state in new_automation.states:  # find all new finishes
        if path_to_finish_by_empty_transitions(state):
            new_automation.finishes.append(state)
 
    return new_automation
 
 
def max_possible_subword(word: str, automation: FiniteAutomation) -> int:
    global_result = 0  # the max length of subword
    for length in range(0, len(word)):
 
        result = 0
        states_from_previous_subword = set(automation.states)
        for symbol in word[length:]: # possггible states for previous subword
            states_for_this_subword = set()  # possible states for current subword
            for state in states_from_previous_subword:
                for transition in automation.transitions:  # try to find possible states for current subword
                    if transition.from_ == state and transition.by == symbol:
                        states_for_this_subword.add(transition.to_)
            if len(states_for_this_subword) == 0:  # no state for this subword -- return result
                break
            else:
                result += 1  # update result
                states_from_previous_subword = states_for_this_subword
 
        if result > global_result:
            global_result = result
    return global_result
 
 
def max_possible_subword_of_expr(expression: str, string: str):
    one_letter_automation = remove_empty_transitions(automation_from_expression(expression))
    return max_possible_subword(string, one_letter_automation)
 
 
if __name__ == '__main__':
    expression = input()
    line = input()
    print(max_possible_subword_of_expr(expression, line))