import grpc
from generated import user_pb2_grpc, user_pb2

def run():
    # Establish a channel to the server
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)

    # Prepare the Empty request
    request = user_pb2.Empty()
    print(request)
    
    try:
        # Call the GetUsers method
        response = stub.GetUsers(request)
        print(response.users)

        # Print the response
        print("Users:")
        for user in response.users:
            print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")

    except grpc.RpcError as e:
        print(f"RPC failed with status code {e.code()}: {e.details()}")

if __name__ == "__main__":
    run()
