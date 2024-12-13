
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# FTP configuration
FTP_PORT = 8087
FTP_USER = "user"
FTP_PASSWORD = "pwd"
FTP_DIRECTORY = "/run/user/1001/gvfs/smb-share:server=10.1.67.156,share=22pw37/sem6/dec"  # Change this to a valid directory in your Linux system

def main():
	# Create an authorizer object to handle user permissions
	authorizer = DummyAuthorizer()
	authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')  # 'elradfmw' grants full permissions
    
	# Create the handler to process FTP requests
	handler = FTPHandler
	handler.authorizer = authorizer
	handler.banner = "pyftpdlib based FTP server is ready."
    
	# Bind the server to the specified address and port (using '0.0.0.0' to listen on all interfaces)
	address = ('10.1.66.47', FTP_PORT)  # Listen on all available interfaces
	server = FTPServer(address, handler)
    
	# Set server limits (optional)
	server.max_cons = 256  # Maximum number of simultaneous connections
	server.max_cons_per_ip = 5  # Maximum number of connections from the same IP
    
	# Start the FTP server
	server.serve_forever()

if __name__ == '__main__':
	main()
