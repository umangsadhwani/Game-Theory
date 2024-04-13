# -*- coding: utf-8 -*-
"""Double_Round_Robin.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1i8K4jpcw41W3ikSMJKfDZpB80Te3Q5mO
"""

def double_round_robin(N, O, U):
    """
    Double Round Robin Algorithm for chore division.

    :param N: Set of agents indexed by integers.
    :param O: Set of items indexed by identifiers.
    :param U: List of dictionaries, each representing an agent's utility for each item.
    :return: Allocation as a dictionary with agents as keys and lists of items as values.
    """
    # Step 1: Initialize the allocation
    allocation = {i: [] for i in N}

    # Step 2: Partition items into O+ and O- based on utility
    O_plus = {o for o in O if any(U[i][o] > 0 for i in N)}
    O_minus = {o for o in O if all(U[i][o] <= 0 for i in N)}

    # Determine the number of dummy chores to create
    a, k = divmod(len(O_minus), len(N))
    dummy_chores = [f'dummy{i}' for i in range(k)]
    O_minus.update(dummy_chores)  # Adding dummy chores to O-

    # Step 4: Round robin sequence for allocating chores in O-
    for i in range(a * len(N) + k):
        agent = N[i % len(N)]
        if O_minus:  # If there are chores to allocate
            allocation[agent].append(O_minus.pop())  # Agent picks a chore (dummy or real)

    # Step 5: Reverse round robin for allocating preferred items in O+
    for i in range(len(O_plus)):
        agent = N[len(N) - 1 - (i % len(N))]  # Reverse order of plus-items
        if O_plus:  # If there are preferred items to allocate
            preferred_item = max(O_plus, key=lambda o: U[agent][o])
            if U[agent][preferred_item] > 0:  # Check if the agent has strictly positive utility
                allocation[agent].append(preferred_item)
                O_plus.remove(preferred_item)
        else:  # No real item gives strictly positive utility
            allocation[agent].append('dummy')  # Pretend to pick a dummy item

    # Step 6: Remove the dummy items from the allocation
    for agent in allocation:
        allocation[agent] = [item for item in allocation[agent] if not item.startswith('dummy')]

    return allocation


# Test cases
agents = [0, 1, 2]
items = ['chore1', 'chore2', 'chore3', 'chore4']
utilities = [
    { 'chore1': -1, 'chore2': -2, 'chore3': 3, 'chore4': 4 },
    { 'chore1': 2, 'chore2': 1, 'chore3': -3, 'chore4': -4 },
    { 'chore1': -2, 'chore2': 3, 'chore3': 1, 'chore4': -1 }
]

allocation = double_round_robin(agents, items, utilities)
print(allocation)