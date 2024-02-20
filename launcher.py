from pathlib import Path
import random
import sys
from typing import List, Tuple

def generate_unique_port(used_ports: set) -> int:
    """Generate a unique port number not in the set of used ports."""
    port = 1024
    while port in used_ports:
        port += 1
    used_ports.add(port)
    return port

def is_valid_domain(domain: str) -> bool:
    """Check if the given domain is valid according to the provided specs."""
    # Check for partial domains
    if len(domain.split('.')) < 3:
        return False

    # Validate characters in domain
    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.")
    if not all(char in valid_chars for char in domain):
        return False

    # Ensure domain doesn't start or end with a dot
    if domain.startswith(".") or domain.endswith("."):
        return False

    return True

def validate_arguments(args: List[str]) -> Tuple[Path, Path]:
    """Validate the command line arguments and return the master file and directory paths."""
    # Check for correct number of arguments
    if len(args) != 2:
        print("INVALID ARGUMENTS")
        sys.exit(1)

    master_file = Path(args[0])
    single_dir = Path(args[1])

    return master_file, single_dir

def validate_master(master_file: Path) -> List[str]:
    """Validate the master file and return its lines if valid."""
    # Check if master file exists
    if not master_file.exists() or not master_file.is_file():
        print("INVALID MASTER")
        sys.exit(1)

    with master_file.open() as file:
        lines = file.readlines()

    # Check if the first line is a valid port
    try:
        port = int(lines[0].strip())
        if port < 1024 or port > 65535:
            raise ValueError
    except ValueError:
        print("INVALID MASTER")
        sys.exit(1)

    domains = {}
    for line in lines[1:]:
        # Skip empty lines or lines with only whitespace
        if not line.strip():
            continue
        try:
            domain, port_str = line.strip().split(',')

            # Validate the domain
            if not is_valid_domain(domain):
                print("INVALID MASTER")
                sys.exit(1)

            port = int(port_str)

            # Check for valid port range
            if port < 1024 or port > 65535:
                print("INVALID MASTER")
                sys.exit(1)

            if domain in domains and domains[domain] != port:
                print("INVALID MASTER")
                sys.exit(1)

            domains[domain] = port

        except ValueError:
            print("INVALID MASTER")
            sys.exit(1)

    return lines


def generate_single_files(master_lines: List[str], single_dir: Path):
    root_port = int(master_lines[0].strip())
    tld_to_authoritative = {}
    authoritative_to_full = {}

    # Set to keep track of used ports
    used_ports = {root_port}
    tld_ports = {}
    authoritative_ports = {}

    for idx, line in enumerate(master_lines[1:], 1):
        domain, port = line.strip().split(',')
        port = int(port)
        used_ports.add(port)
        parts = domain.split('.')
        tld = parts[-1]
        authoritative = parts[-2] + '.' + tld

        if tld not in tld_to_authoritative:
            tld_to_authoritative[tld] = set()
            tld_ports[tld] = generate_unique_port(used_ports)
        tld_to_authoritative[tld].add(authoritative)

        if authoritative not in authoritative_to_full:
            authoritative_to_full[authoritative] = []
            authoritative_ports[authoritative] = generate_unique_port(used_ports)
        authoritative_to_full[authoritative].append((domain, port))

    filename_root = "000_" + f"{random.randint(0, 999999):06}.conf"
    with (single_dir / filename_root).open('w') as root_file:
        root_file.write(str(root_port) + "\n")
        for tld in sorted(tld_to_authoritative.keys()):
            root_file.write(f"{tld},{tld_ports[tld]}\n")

    for tld, authoritatives in sorted(tld_to_authoritative.items()):
        filename_tld = "tld_" + tld + "_" + f"{random.randint(0, 999999):06}.conf"
        with (single_dir / filename_tld).open('w') as tld_file:
            tld_file.write(str(tld_ports[tld]) + "\n")
            for authoritative in authoritatives:
                tld_file.write(f"{authoritative},{authoritative_ports[authoritative]}\n")

    for authoritative, full_domains in sorted(authoritative_to_full.items()):
        primary_domain, primary_port = full_domains[0]
        filename_auth = authoritative.replace('.', '_') + "_" + f"{random.randint(0, 999999):06}.conf"
        with (single_dir / filename_auth).open('w') as auth_file:
            auth_file.write(str(authoritative_ports[authoritative]) + "\n")
            for full_domain, port in full_domains:
                auth_file.write(f"{full_domain},{port}\n")


def main(args: List[str]) -> None:
    #print(f"Received arguments: {args}")  # Print the received arguments for debugging

    master_file, single_dir = validate_arguments(args)

    # Check if the directory exists and is writable
    if not single_dir.exists() or not single_dir.is_dir():
        print("NON-WRITABLE SINGLE DIR")
        return

    master_lines = validate_master(master_file)


    generate_single_files(master_lines, single_dir)

if __name__ == "__main__":
    main(sys.argv[1:])