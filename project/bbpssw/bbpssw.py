import math
from copy import copy

from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.external import get_qubit_state
from netqasm.sdk.toolbox.sim_states import qubit_from, to_dm, get_fidelity

def bbpssw_protocol_alice(q1, q2, alice, socket):
    """
    Implements Alice's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for BBPSSW using
    qubits q1 and q2, then send the measurement outcome to Bob and determine
    if the distillation was successful.
    
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param alice: Alice's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    a = bbpssw_gates_and_measurement_alice(q1, q2)
    alice.flush()

    # Write below the code to send measurement result to Bob,
    # receive measurement result from Bob and check if protocol was successful
    socket.send_structured(StructuredMessage("The measurement outcome of Alice is:", int(a)))
    b = socket.recv_structured().payload

    dm1 = get_qubit_state(q1)
    print(f'=====ALICE AFTER=====')
    # print(f'Alice has dm_1 as:')
    # print(f'{dm1}')

    target = qubit_from(0, 0)
    # tdm = to_dm(target)

    # print(f'Alice has t_dm as:')
    # print(f'{tdm}')

    f1 = get_fidelity(target, dm1)
    print(f'Alice has f1: {f1}')

    print(f'Measurement Alice: {a}')

    if a.value == b:
        return True
    return False


def bbpssw_gates_and_measurement_alice(q1, q2):
    """
    Performs the gates and measurements for Alice's side of the BBPSSW protocol
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :return: Integer 0/1 indicating Alice's measurement outcome
    """
    q1.cnot(q2)

    return q2.measure()


def bbpssw_protocol_bob(q1, q2, bob, socket):
    """
    Implements Bob's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for BBPSSW using
    qubits q1 and q2, then send the measurement outcome to Alice and determine
    if the distillation was successful.
    
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param bob: Bob's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    b = bbpssw_gates_and_measurement_bob(q1, q2)
    bob.flush()

    # Write below the code to send measurement result to Alice,
    # receive measurement result from Alice and check if protocol was successful
    socket.send_structured(StructuredMessage("The measurement outcome of Bob is:", int(b)))
    a = socket.recv_structured().payload

    dm1 = get_qubit_state(q1)
    # dm2 = get_qubit_state(q2)
    print(f'=====BOB AFTER=====')
    # print(f'Bob has dm_1 as:')
    # print(f'{dm1}')

    target = qubit_from(0, math.pi)
    # tdm = to_dm(target)

    # print(f'Bob has t_dm as:')
    # print(f'{tdm}')

    f1 = get_fidelity(target, dm1)
    print(f'Bob has f1: {f1}')

    print(f'Measurement Bob: {b}')

    if a == b.value:
        return True
    return False


def bbpssw_gates_and_measurement_bob(q1, q2):
    """
    Performs the gates and measurements for Bob's side of the BBPSSW protocol
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :return: Integer 0/1 indicating Bob's measurement outcome
    """
    q1.cnot(q2)
    q2.H()

    return q2.measure()

