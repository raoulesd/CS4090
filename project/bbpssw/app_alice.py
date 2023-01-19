from bbpssw import bbpssw_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket

def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket("alice", "bob")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
    )

    # Create Alice's context, initialize EPR pairs inside it and call Alice's BBPSSW method.
    # Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:

        # Create the two EPR pairs
        epr_1 = epr_socket.create()[0]
        epr_2 = epr_socket.create()[0]

        # Call the BBPSSW method
        res = bbpssw_protocol_alice(epr_1, epr_2, alice, socket)

        print(f'Result Alice: {res}')

if __name__ == "__main__":
    main()
