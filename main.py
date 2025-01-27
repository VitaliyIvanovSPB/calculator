import math
from data import cpus_intel, cpus_amd


def requested_config(vcpu: int, vram: int, vssd: int, cpu_overcommit: int = 3, cpu_vendor: str = 'any',
                     cpu_min_frequency: int = 0, max_cpu_usage: float = 0.8, max_ram_usage: float = 0.8):
    # cpu_hosts(n + 1)
    #
    # ram_hosts = vRAM / кол - во
    # RAM
    # в
    # хосте * RAM
    # max
    # usage

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
                if cpu_min_frequency < cpu['cores_frequency']:
                    vcpu_on_host = cpu['cores_quantity'] * 2 * max_cpu_usage
                    cpu_hosts = math.ceil(vcpu / cpu_overcommit / vcpu_on_host)
                    ram_host=
                    print(
                        f"CPU name = {cpu['name']}, need host by cpu = {cpu_hosts}, total price = {cpu_hosts * cpu['price']} $")
                    total_config.append()
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
    print(requested_config(vcpu=4000, vram=16000, vssd=100000, cpu_vendor='intel', cpu_min_frequency = 2300))

# TODO:
# вся логика пока только на интеле