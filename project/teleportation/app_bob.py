from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket

def main(app_config=None):

    # Socket initialisation
    socket = Socket("bob", "alice")

    # EPR socket
    epr_socket = EPRSocket("alice")

    # Initialisation with NetQASM backend
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
    )

    with bob:

        # Create EPR pair
        epr = epr_socket.recv()[0]

        # Teleportation operations
        m1, m2 = socket.recv_structured().payload

        #Apply corrections
        if m2 == 1:
            epr.X()
        if m1 == 1:
            epr.Z()

        result = epr.measure()
        bob.flush()

        print(f'Bob: {result}')


if __name__ == "__main__":
    main()