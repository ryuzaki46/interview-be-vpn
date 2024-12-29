import os
import sys
import threading
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application
from uvicorn import Config, Server

# Load environment variables
load_dotenv()

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_backend.settings')

# Add the parent directory to the Python path to access grpc_app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ensure Django setup before any Django-related code
import django
django.setup()

# Import gRPC services after Django is set up
from grpc_app.services import serve_grpc

# Create the ASGI application instance
application = get_asgi_application()

def run_grpc():
    print("Starting gRPC server...")
    serve_grpc()
    print("gRPC server running...")

if __name__ == "__main__":
    # Start gRPC server in a separate thread
    grpc_thread = threading.Thread(target=run_grpc)
    grpc_thread.daemon = True
    grpc_thread.start()

    # Start the ASGI application server (Django)
    config = Config(app=application, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
    server = Server(config)
    server.run()  # Run the server in the main thread
