import math
from data import cpus_intel, cpus_amd, rams, servers


def requested_config(cpu_vendor: str = 'any', vcpu: int = 400, vram: int = 800, vssd: int = 20000,
                     cpu_overcommit: int = 3, cpu_min_frequency: int = 0, max_cpu_usage: float = 0.8,
                     max_ram_usage: float = 0.8):
    all_configs = {}
    match cpu_vendor:
        case 'any':
            for cpu in cpus_intel:
                vcpu_on_host = cpu['cores_quantity'] * 2 * max_cpu_usage
                cpu_hosts = math.ceil(vcpu / cpu_overcommit / vcpu_on_host)
                print(
                    f"CPU name = {cpu['name']}, need host by cpu = {cpu_hosts}, total price = {cpu_hosts * cpu['price']} $")
            for cpu in cpus_amd:
                vcpu_on_host = cpu['cores_quantity'] * 2 * max_cpu_usage
                cpu_hosts = math.ceil(vcpu / cpu_overcommit / vcpu_on_host)
                print(
                    f"CPU name = {cpu['name']}, need host by cpu = {cpu_hosts}, total price = {cpu_hosts * cpu['price']} $")
        case 'intel':
            for cpu in cpus_intel:
                if cpu_min_frequency < cpu['cores_frequency']:
                    cpu_hosts = math.ceil(vcpu / cpu_overcommit / (cpu['cores_quantity'] * 2 * max_cpu_usage))
                    for server in servers:
                        if server['socket'] == cpu['socket']:
                            for ram in rams:
                                if server['ram_gen'] == ram['ram_gen']:
                                    ram_host = math.ceil(vram / max_ram_usage / cpu_hosts / ram['ram_size'])
                                    ram_1host = ram_host + 1 if ram_host % 2 == 1 else ram_host
                                    if ram_1host > server['max_ram']:
                                        continue
                                    all_configs[len(all_configs)] = {'Need hosts by CPU:': cpu_hosts,
                                                                     'CPU:': cpu['name'],
                                                                     'Server: ': server['name'],
                                                                     ram['ram_size']: ram_1host}
                        else:
                            continue
                else:
                    continue
            return all_configs
        case 'amd':
            for cpu in cpus_amd:
                vcpu_on_host = cpu['cores_quantity'] * 2 * max_cpu_usage
                cpu_hosts = math.ceil(vcpu / cpu_overcommit / vcpu_on_host)
                print(
                    f"CPU name = {cpu['name']}, need host by cpu = {cpu_hosts}, total price = {cpu_hosts * cpu['price']} $")
        case _:
            return 'хз кто это!'


if __name__ == '__main__':
    print(requested_config(vcpu=4000, vram=16000, vssd=100000, cpu_vendor='intel', cpu_min_frequency=3600))

# TODO:
# вся логика пока только на интеле
