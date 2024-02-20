"""
Write code for your verifier here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
import sys
from pathlib import Path
from typing import List, Dict

def extract_domain_from_filename(filename: str) -> str:
    # Remove extensions and digits
    clean_name = ''.join([c for c in filename if not c.isdigit()]).replace('.conf', '')
    # Replace underscores with dots
    domain = clean_name.replace('_', '.')
    # If we end up with tld.domain, we only want the domain
    if domain.startswith('tld.'):
        domain = domain.split('.')[1]
    return domain

def is_valid_hostname(hostname: str) -> bool:
    parts = hostname.split('.')
    if len(parts) < 2:
        return False
    for part in parts:
        if not part.isalnum() and not (part[0].isalnum() and part[-1].isalnum() and all(ch.isalnum() or ch == '-' for ch in part)):
            return False
    return True

def validate_master_config(master_config: List[str]) -> bool:
    try:
        master_port = int(master_config[0].strip())
        if not (1024 <= master_port <= 65535):
            return False
    except ValueError:
        return False
    
    for line in master_config[1:]:
        if not line.strip():
            continue

        try:
            domain, port = line.strip().split(',')
        except ValueError:
            return False
        
        # Check if the domain has only one "."
        if domain.count('.') == 1:
            return False
        
        if not is_valid_hostname(domain):
            return False
        
        try:
            if not (1024 <= int(port) <= 65535):
                return False
        except ValueError:
            return False
    return True


def read_single_configs(directory_of_single_files: Path) -> Dict[str, List[str]]:
    single_configs = {}
    for single_file in directory_of_single_files.iterdir():
        if single_file.is_file():
            domain_key = extract_domain_from_filename(single_file.name)
            with single_file.open('r') as file:
                lines = file.readlines()
                single_configs[domain_key] = lines
    return single_configs


def compare_configs(master_config: List[str], single_configs: Dict[str, List[str]]) -> bool:
    master_mappings = {line.split(',')[0]: int(line.split(',')[1]) for line in master_config[1:]}

    all_domain_mappings = {}
    tld_domain_mappings = {}
    tld_file_ports = set()  # To store the ports at the top of TLD configuration files
    
    for single_file, config in single_configs.items():
        single_port = int(config[0])
        
        # Check if the port is within the range
        if not (1024 <= single_port <= 65535):
            print("invalid single")
            sys.exit()

        domain_mappings = {line.split(',')[0]: int(line.split(',')[1]) for line in config[1:]}

        # Additional check for ports in the mappings
        for _, port in domain_mappings.items():
            if not (1024 <= port <= 65535):
                print("invalid single")
                sys.exit()

        domain_key = extract_domain_from_filename(single_file)
        tld_domain_mappings[domain_key] = single_port
        
        if single_file.startswith("tld-"):
            # Check for uniqueness of the port at the top of the TLD configuration files
            if single_port in tld_file_ports:
                return False
            tld_file_ports.add(single_port)
        
        all_domain_mappings.update(domain_mappings)

    # Checking the TLD mappings against root.conf
    for tld, port in tld_domain_mappings.items():
        if tld in master_mappings and master_mappings[tld] != port:
            return False

    # Checking the TLD mappings against other single_configs
    for tld, port in tld_domain_mappings.items():
        if tld in all_domain_mappings and all_domain_mappings[tld] != port:
            return False

    # Checking all other mappings
    for domain, port in master_mappings.items():
        if domain not in all_domain_mappings or all_domain_mappings[domain] != port:
            return False

    return True


def main(args: List[str]) -> None:
    if len(args) != 2:
        print("invalid arguments")
        sys.exit()

    master_file, directory_of_single_files = args

    master_path = Path(master_file)
    if not master_path.exists() or not master_path.is_file():
        print("invalid master")
        sys.exit()

    single_files_dir = Path(directory_of_single_files)
    if not single_files_dir.exists() or not single_files_dir.is_dir():
        print("singles io error")
        sys.exit()

    with master_path.open('r') as file:
        master_config = file.readlines()
    
    #print("=== Master Configuration ===")
    #print(''.join(master_config))
    #print("============================")
    
    if not validate_master_config(master_config):
        print("invalid master")
        sys.exit()

    try:
        single_configs = read_single_configs(single_files_dir)
    except Exception as e:
        print("invalid single")
        sys.exit()

    if compare_configs(master_config, single_configs):
        print("eq")
    else:
        print("neq")

if __name__ == "__main__":
    main(sys.argv[1:])