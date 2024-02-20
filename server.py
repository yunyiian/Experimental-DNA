"""
Write code for your server here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from typing import Tuple, Dict, List
from sys import argv
import socket

def is_valid_hostname(hostname: str) -> bool:
    """
    Check if the given hostname is valid.
    """
    parts = hostname.split('.')
    
    if len(parts) == 1:
        # A
        return parts[0].isalnum() or (all(c.isalnum() or c == '-' for c in parts[0]) and not (parts[0].startswith('-') or parts[0].endswith('-')))
    elif len(parts) == 2:
        # B.A
        return all(part.isalnum() or (all(c.isalnum() or c == '-' for c in part) and not (part.startswith('-') or part.endswith('-'))) for part in parts)
    elif len(parts) > 2:
        # C.B.A
        if not parts[-1].isalnum() or not parts[-2].isalnum():
            return False
        for part in parts[:-2]:
            if not part.isalnum() and not all(c.isalnum() or c == '-' for c in part):
                return False
            if part.startswith('-') or part.endswith('-') or part.startswith('.') or part.endswith('.'):
                return False
        return True
    return False

def read_server_config(config_file_path: str) -> Tuple[int, Dict[str, int]]:
    domain_mappings = {}
    try:
        with open(config_file_path, 'r') as file:
            lines = file.readlines()
            server_port = int(lines[0].strip())

            # Validate server port
            if server_port < 1024 or server_port > 65535:
                print("INVALID CONFIGURATION")
                return -1, {}

            for line in lines[1:]:
                domain, port = line.strip().split(',')
                
                # Check for valid domain name
                if not is_valid_hostname(domain):
                    print("INVALID CONFIGURATION")
                    return -1, {}

                # Check for valid port
                if not port.isdigit() or int(port) < 1024 or int(port) > 65535:
                    print("INVALID CONFIGURATION")
                    return -1, {}

                # Check for contradicting records
                if domain in domain_mappings and domain_mappings[domain] != int(port):
                    print("INVALID CONFIGURATION")
                    return -1, {}

                domain_mappings[domain] = int(port)
    except FileNotFoundError:
        print("INVALID CONFIGURATION")
        return -1, {}
    except Exception as e:
        print("INVALID CONFIGURATION")
        return -1, {}
    return server_port, domain_mappings


def handle_domain_query(domain: str, domain_mappings: dict) -> str:
    if not is_valid_hostname(domain):
        print("INVALID")
        return "INVALID"

    response = str(domain_mappings.get(domain, "NXDOMAIN"))
    print(f"resolve {domain} to {response}")
    return response


def handle_command(command: str, domain_mappings: dict) -> str:
    tokens = command.split()
    cmd_type = tokens[0]

    if cmd_type == "!ADD":
        if len(tokens) != 3:
            return "INVALID"
        hostname, port = tokens[1], tokens[2]
        if not is_valid_hostname(hostname):
            return "INVALID"
        if not port.isdigit() or int(port) < 1024 or int(port) > 65535:
            return "INVALID"
        if int(port) in domain_mappings.values():
            return "INVALID"
        domain_mappings[hostname] = int(port)
        return ""

    elif cmd_type == "!DEL":
        if len(tokens) != 2:
            return "INVALID"
        hostname = tokens[1]
        if not is_valid_hostname(hostname):
            return "INVALID"
        domain_mappings.pop(hostname, None)
        return ""

    elif cmd_type == "!EXIT":
        return "SHUTDOWN"

    else:
        return "INVALID"

def start_server_socket(port: int, domain_mappings: dict) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', port)
    server_socket.bind(server_address)
    server_socket.listen(1)

    incomplete_message = ""

    try:
        while True:
            connection, client_address = server_socket.accept()
            try:
                data = connection.recv(1024).decode('utf-8')
                message = incomplete_message + data

                if not message.endswith('\n'):
                    incomplete_message = message
                    continue

                incomplete_message = ""  # Clear buffer

                if message.startswith('!'):
                    response = handle_command(message.strip(), domain_mappings)
                    if response == "SHUTDOWN":
                        break
                    elif response:
                        connection.sendall((response + "\n").encode('utf-8'))
                else:
                    response = handle_domain_query(message.strip(), domain_mappings)
                    connection.sendall((response + "\n").encode('utf-8'))
            except socket.error:
                # Handle socket errors gracefully
                print("Socket error occurred!")
            finally:
                connection.close()
    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()

def main(args: List[str]) -> None:
    if not args or len(args) > 1:
        print("INVALID ARGUMENTS")
        return

    port, domain_mappings = read_server_config(args[0])
    if port != -1:
        start_server_socket(port, domain_mappings)

if __name__ == "__main__":
    main(argv[1:])
