import time
from main import connect_to_hosts, check_ssh_connect, execute_sudo_command
from config import *
def generate_client_keys(function_connect):
    commands = [
        f'wg genkey | tee {path_to_config}{client_name}_privatekey | wg pubkey | tee {path_to_config}{client_name}_publickey'
    ]

    for command in commands:
        print(f"Executing as sudo {command}")
        execute_sudo_command(function_connect, command)
        time.sleep(2)

def add_client_to_wg0conf(function_connect):
    commands = [
        f'echo "" | sudo tee -a {path_to_config}wg0.conf',
        f'echo "[Peer]" | sudo tee -a {path_to_config}wg0.conf',
        f'echo "#{client_name}" | sudo tee -a {path_to_config}wg0.conf',
        f'echo "PublicKey = $(cat {path_to_config}ira_publickey)" | sudo tee -a {path_to_config}wg0.conf',
        f'echo "AllowedIPs = {client_ip}/32" | sudo tee -a {path_to_config}wg0.conf',
        'systemctl restart wg-quick@wg0'
    ]

    for command in commands:
        print(f"Executing as sudo {command}")
        execute_sudo_command(function_connect, command)
        time.sleep(2)


def create_client_conf(function_connect):
    commands = [
        f'echo "[Interface]" | sudo tee -a {path_to_config}{client_name}.conf',
        f'echo "Address = {client_ip}/32" | sudo tee -a {path_to_config}{client_name}.conf',
        f'echo "PrivateKey = $(cat {path_to_config}{client_name}_privatekey)" | sudo tee -a {path_to_config}{client_name}.conf',
        f'echo "" | sudo tee -a {path_to_config}{client_name}.conf',
        f'echo "[Peer]" | sudo tee -a {path_to_config}{client_name}.conf',
        f'echo "PublicKey = $(cat {path_to_config}publickey)" | sudo tee -a {path_to_config}{client_name}.conf',
        f'echo "Endpoint = {wireguard_ip}:{wireguard_port}" | sudo tee -a {path_to_config}{client_name}.conf',
        f'echo "AllowedIPs = {AllowedIPs}" | sudo tee -a {path_to_config}{client_name}.conf'
    ]

    for command in commands:
        print(f"Executing as sudo {command}")
        execute_sudo_command(function_connect, command)
        time.sleep(2)


client_name = input('\033[34mEnter username of a new client:\033[0m ')
client_ip = input(f'\033[34mCheck free IP address in {path_to_config}wg0.conf and Enter IP address for a new client:\033[0m ')

if check_ssh_connect(hip_hosting):
    for host in hip_hosting:
        print(f"\033[44m Check host {host}\033[0m")
        connect = connect_to_hosts(host)
        generate_client_keys(connect)
        create_client_conf(connect)
        add_client_to_wg0conf(connect)
        connect.close()

