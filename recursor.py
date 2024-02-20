"""
Write code for your recursor here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
import socket
import sys

def validate_domain(domain: str) -> bool:
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.")
    return (
        all(char in allowed_chars for char in domain) and
        not domain.startswith(".") and
        not domain.endswith(".") and
        not domain.startswith("-") and
        not domain.endswith("-") and
        ".." not in domain and
        domain.count(".") >= 2 
    )

def query_domain(domain: str, root_port: int, timeout: float) -> str:
    domain_parts = domain.split('.')
    
    try:
        # Step 1: Query the root DNS server
        with socket.create_connection(("localhost", root_port), timeout=timeout) as s:
            s.sendall((domain_parts[-1] + "\n").encode('utf-8'))
            response = s.recv(1024).decode('utf-8').strip()
        if response == "NXDOMAIN":
            return response
        next_port = int(response)
    except socket.timeout:
        return "NXDOMAIN"
    except ConnectionRefusedError:
        print("FAILED TO CONNECT TO ROOT")
        sys.exit(1)
    
    try:
        # Step 2: Query the TLD DNS server
        with socket.create_connection(("localhost", next_port), timeout=timeout) as s:
            s.sendall((domain_parts[-2] + "." + domain_parts[-1] + "\n").encode('utf-8'))
            response = s.recv(1024).decode('utf-8').strip()
        if response == "NXDOMAIN":
            return response
        next_port = int(response)
    except socket.timeout:
        return "NXDOMAIN"
    except ConnectionRefusedError:
        print("FAILED TO CONNECT TO TLD")
        sys.exit(1)

    # Step 3: Query the authoritative DNS server if there are more than 2 domain parts
    if len(domain_parts) > 2:
        try:
            with socket.create_connection(("localhost", next_port), timeout=timeout) as s:
                s.sendall((domain + "\n").encode('utf-8'))
                response = s.recv(1024).decode('utf-8').strip()
                if response == "NXDOMAIN":
                    return response
                resolved_port = int(response.strip())  # Check if it can be converted to int
                return str(resolved_port)
        except ValueError:  # In case the response is not a valid port number
            return "NXDOMAIN"
        except socket.timeout:
            return "NXDOMAIN"
        except ConnectionRefusedError:
            print("FAILED TO CONNECT TO AUTH")
            sys.exit(1)
    else:
        return "NXDOMAIN"



def main(args: list[str]) -> None:
    if len(args) != 2:
        print("INVALID ARGUMENTS")
        sys.exit(1)

    try:
        root_port = int(args[0])
        timeout = float(args[1])
    except ValueError:
        print("INVALID ARGUMENTS")
        sys.exit(1)
        
    if not (1024 <= root_port <= 65535):
        print("INVALID ARGUMENTS")
        sys.exit(1)

    try:
        while True:
            domain = input()
            if validate_domain(domain):
                resolved_port = query_domain(domain, root_port, timeout)
                print(resolved_port)
            else:
                print("INVALID")
    except EOFError:
        pass
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
