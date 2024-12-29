import os
import grpc
from concurrent import futures
from .generated import user_pb2, user_pb2_grpc
from .models import User


class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUsers(self, request, context):
        # Get Data User when call from GRPC
        users = User.objects.all()
        print(User.objects.count())
        user_list = [user_pb2.User(id=user.id, name=user.username, email=user.email) for user in users]
        return user_pb2.UserList(users=user_list)

def serve_grpc():
    # For running GRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    grpc_host = os.getenv("HOST_GRPC", "localhost:50051")    
    server.add_insecure_port(grpc_host)
    print("gRPC server started, listening on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve_grpc()