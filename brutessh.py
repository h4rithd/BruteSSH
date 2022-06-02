import time
import socket
import paramiko
import textwrap
import argparse
from colorama import init, Fore

init()

GREEN = Fore.GREEN
RED   = Fore.RED
RESET = Fore.RESET
BLUE  = Fore.BLUE

def sshLoginCheck(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        print(f"{RED}[ ERROR ] {hostname}\tIs unreachable, timed out.{RESET}")
        open("logs.txt","a").write(f"[ ERROR ] {hostname}\tis unreachable, timed out!\n")
        return True
    except paramiko.AuthenticationException:
        print(f"{RED}[INVALID] {hostname}\tInvalid credentials found [{username}:{password}] {RESET}")
        open("logs.txt","a").write(f"[INVALID] {hostname}\tInvalid credentials found [{username}:{password}]\n")
        return True
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(f"{RED}[ ERROR ] {hostname}\tUnable to connect to port 22 {RESET}")
        open("logs.txt","a").write(f"[ ERROR ] {hostname}\tUnable to connect to port 22\n")
        return True
    except paramiko.SSHException:
        print(f"{BLUE}[ ERROR ] Quota exceeded!, Retrying with delay...{RESET}")
        time.sleep(60)
        return sshLoginCheck(hostname, username, password)
    else:
        print(f"{GREEN}[SUCCESS] {hostname}\tLogin successful [{username}:{password}]{RESET}")
        return False

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
    prog='brutessh.py',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
    -------------------------------------------------------------
    --------------- | Bulk SSH Login check |---------------------
    -------------------------------------------------------------
                ▙ 🆁 ▙▟ ▜▛ █☰ ▟▛ ▟▛ █▬█
                                          V 0.1
    by h4rith.com
    -------------------------------------------------------------'''),
    usage='python3 %(prog)s -i [iplist] -u [username] -p [password]',
    epilog='---------------- Script from h4rithd.com ----------------'
    )
    
    parser._action_groups.pop()
    required = parser.add_argument_group('[!] Required arguments')
    optional = parser.add_argument_group('[!] Optional arguments')

    required.add_argument("-i", "--iplist", metavar='', required=True, help="File that contain list of IP Address.") 
    required.add_argument("-p", "--password", metavar='', required=True, help="Valid Password.") 

    optional.add_argument("-u", "--username", metavar='', default="root", help='Valid Username.')

    args = parser.parse_args()

    iplist = args.iplist
    password = args.password
    username = args.username
    iplist = open(iplist).read().splitlines()

    for host in iplist:
        if sshLoginCheck(host,username,password):
            continue
