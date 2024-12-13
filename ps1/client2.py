import ftplib

# FTP Server details
HOSTNAME = "10.1.66.47"  # The IP address of your FTP server
PORT = 8087
USERNAME = "user"  # FTP username
PASSWORD = "pwd"  # FTP password

# Establish FTP connection on port 8087
ftp_server = ftplib.FTP()
ftp_server.connect(HOSTNAME, PORT)  # Specify the correct port
ftp_server.login(USERNAME, PASSWORD)
ftp_server.encoding = "utf-8"

# Upload a file
filename = "login.txt"
with open(filename, "rb") as file:
    ftp_server.storbinary(f"STOR {filename}", file)

# List the contents of the current directory
ftp_server.dir()

# Close the connection
ftp_server.quit()
