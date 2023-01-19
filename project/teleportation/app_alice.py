from netqasm.sdk import Qubit, EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk.classical_communication.message import StructuredMessage

def main(app_config=None):

    # Socket initialisation
    socket = Socket("alice", "bob")

    # EPR socket
    epr_socket = EPRSocket("bob")

    # Initialisation with NetQASM backend
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
    )

    with alice:

        # Create qubit
        q = Qubit(alice)

        # Create EPR pair
        epr = epr_socket.create()[0]

        # Teleportation operations

        q.cnot(epr)
        q.H()
        m1 = q.measure()
        m2 = epr.measure()

        alice.flush()

        m1, m2 = int(m1), int(m2)

        socket.send_structured(StructuredMessage(f'The corrections are:', (m1, m2)))


if __name__ == "__main__":
    main()
