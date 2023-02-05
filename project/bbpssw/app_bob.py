import time
from bbpssw import bbpssw_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket

def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket("bob", "alice")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("alice")

    # Initialize Bob's NetQASM connection
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's BBPSSW method.
    # Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:

        # Create EPR pair
        epr_1 = epr_socket.recv()[0]
        epr_2 = epr_socket.recv()[0]

        # Call the BBPSSW method
        res = bbpssw_protocol_bob(epr_1, epr_2, bob, socket)

        print(f'Result Bob: {res}')


if __name__ == "__main__":
    main()
    time.sleep(1)

