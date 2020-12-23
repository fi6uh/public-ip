import subprocess
import ipaddress
import argparse


def run_cmd(cmd):
    results = ""
    try:
        results = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError as e:
        x = 1
    return results


def get_trace_ip(n, iface):
    cmd = "traceroute -i " + str(iface) + " -f 1 -M 1 -m " + str(n) + " -q 1 -n 9.9.9.9"
    ip = run_cmd(cmd).strip().split('\n')[-1].split()[1]
    if ip == '*':
        ip = "127.0.0.1"
    return ip


def cidrmatch(ip, subnet):
    return ipaddress.ip_address(ip) in ipaddress.ip_network(subnet) or ip=="127.0.0.1"


def is_local_ip(ip, cidr_list):
    matches = []
    for cidr in cidr_list:
           matches.append(cidrmatch(ip, cidr))
    return True in matches


def looproute(cidr_list, iface="en0"):
    n = 1
    while True:
        ip = get_trace_ip(n, iface)
        if is_local_ip(ip, cidr_list):
            n += 1
        else:
            break
    return ip


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iface", help="Interface to run traceroute on; defaults to en0")
    args = parser.parse_args()

    cidr_list = ["10.0.0.0/8", "172.16.0.0/16", "192.168.0.0/16"]
    if args.iface:
        ip = looproute(cidr_list, args.iface)
    else:
        ip = looproute(cidr_list)
    print(ip)


if __name__ == "__main__":
    main()
