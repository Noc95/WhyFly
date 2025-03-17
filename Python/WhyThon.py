import socket

# These must match the Pico W's settings
WHYFLY_IP = "192.168.42.1"  # The AP's sacred address
PORT = 80                # The port of the Wi-Fi server

def fetch_pico_message():
    """Connecteth to the Pico W and retrieveth its message."""
    try:
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Seeking the wisdom of Pico W...")
            s.connect((WHYFLY_IP, PORT))  # Connect to the server
            
            # Receive the divine message
            data = s.recv(1024)  # Read up to 1024 bytes
            print("Lo! The Pico W hath spoken:")
            print(data.decode())  # Decode and display the message
    
    except Exception as e:
        print("Alas! An error hath occurred:", e)

# Call the function to fetch data
fetch_pico_message()
