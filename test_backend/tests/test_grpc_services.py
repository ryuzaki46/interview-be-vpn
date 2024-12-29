import grpc
from grpc_app.generated import user_pb2, user_pb2_grpc
import unittest

class TestGrpcServer(unittest.TestCase):
    def test_grpc_service(self):
        # Create a channel and a stub
        channel = grpc.insecure_channel('localhost:50051')
        stub = user_pb2_grpc.UserServiceStub(channel)
        
        # Create a request
        request = user_pb2.Empty()

        # Make the gRPC call
        response = stub.GetUsers(request)
        # Assert that the response contains users
        self.assertIsNotNone(response)
        self.assertGreater(len(response.users), 0)  # Assuming at least one user exists in the DB
        
        # Optional: Check the data of the first user
        self.assertEqual(response.users[0].name, "testuser")
        self.assertEqual(response.users[0].email, "testuser@example.com")

if __name__ == '__main__':
    unittest.main()
