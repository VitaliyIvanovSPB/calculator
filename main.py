import math
from data import cpus_intel, cpus_amd, ram, servers

ram_size_32 = 32


def requested_config(vcpu: int, vram: int, vssd: int, cpu_overcommit: int = 3, cpu_vendor: str = 'any',
                     cpu_min_frequency: int = 0, max_cpu_usage: float = 0.8, max_ram_usage: float = 0.8):
    total_config = []
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
            return total_config
        case 'intel':
            for cpu in cpus_intel:
                i = 1
                full_config = {}
                if cpu_min_frequency < cpu['cores_frequency']:
                    cpu_hosts = math.ceil(vcpu / cpu_overcommit / (cpu['cores_quantity'] * 2 * max_cpu_usage))
                    for server in servers:
                        if server['socket'] == cpu['socket']:
                            full_config[i] = {'CPU:': cpu['name']}
                            full_config[i].update({'Need hosts by CPU:': cpu_hosts})
                            full_config[i].update({'Server: ': server['name']})
                            ram32_host = math.ceil(vram / max_ram_usage / cpu_hosts / ram_size_32)
                            ram32_1host = ram32_host + 1 if ram32_host % 2 == 1 else ram32_host
                            full_config[i].update({'32gb RAM: ': ram32_1host})
                            full_config[i].update(
                                {'cost: ': (cpu['price'] + server['price'] + +ram32_1host * 120) * cpu_hosts})
                            i += 1

                else:
                    continue

                total_config.append(full_config)
            return total_config
        case 'amd':
            for cpu in cpus_amd:
                vcpu_on_host = cpu['cores_quantity'] * 2 * max_cpu_usage
                cpu_hosts = math.ceil(vcpu / cpu_overcommit / vcpu_on_host)
                print(
                    f"CPU name = {cpu['name']}, need host by cpu = {cpu_hosts}, total price = {cpu_hosts * cpu['price']} $")
            return total_config
        case _:
            return 'хз кто это!'


if __name__ == '__main__':
    print(requested_config(vcpu=4000, vram=16000, vssd=100000, cpu_vendor='intel', cpu_min_frequency=3600))

# TODO:
# вся логика пока только на интеле
