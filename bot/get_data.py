import sqlite3
from collections import defaultdict

DB_PATH = 'bot/data.db'


# DB_PATH = 'data.db'


def get_parameters():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT param_name, param_value FROM parameters")
        return {row[0]: float(row[1]) for row in cursor.fetchall()}


def get_works_coefficient():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT service, hosts_8, hosts_16, hosts_24, hosts_32, hosts_64, hosts_96, hosts_128 FROM works_coefficient")
        return {row[0]: list(row[1:]) for row in cursor.fetchall()}


def get_raid_config():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT raid_level, FTM, FTT, disk_usage_overhead FROM raid_config")
        return {row[0]: {'FTM': row[1], 'FTT': row[2], 'disk_usage_overhead': row[3]} for row in cursor.fetchall()}


def get_raids_data():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT raid_type, level, item_id, value_id, value FROM raids')
        raids_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        for raid_type, level, item_id, value_id, value in cursor.fetchall():
            raids_data[raid_type][level][item_id][value_id] = value
        return {raid_type: {level: {item_id: dict(values) for item_id, values in items.items()} for level, items in
                            levels.items()} for raid_type, levels in raids_data.items()}


def get_cpus_filtered(cpu_vendor='any', cpu_min_frequency=0):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM cpus WHERE cores_frequency >= ?"
        params = [cpu_min_frequency]

        if cpu_vendor != 'any':
            query += " AND manufacturer = ?"
            params.append(cpu_vendor)

        cursor.execute(query, params)

        return [
            {
                'manufacturer': row[1],
                'name': row[2],
                'cores_quantity': row[3],
                'cores_frequency': row[4],
                'price': row[5],
                'socket': row[6],
                'ram_gen': row[7]
            }
            for row in cursor.fetchall()
        ]


def get_servers_filtered(socket_filter=3647):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servers WHERE socket = ?", (socket_filter,))

        return [
            {
                'name': row[1],
                'cpu_vendor': row[2],
                'socket': row[3],
                'max_ram': row[4],
                'ram_gen': row[5],
                'max_disks_qty': row[6],
                'price': row[7]
            }
            for row in cursor.fetchall()
        ]


def get_esxi_disks():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM esxi_disks')
        return {row[1]: {'disk_type': row[2], 'price': row[3]} for row in cursor.fetchall()}


def get_cache_disks():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cache_disks')
        return [{'disk_type': row[1], 'capacity': row[2], 'price': row[3]} for row in cursor.fetchall()]


def get_network_cards():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM network_cards')
        return [{'name': row[1], 'price': row[2]} for row in cursor.fetchall()]


def get_hba_adapters():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM hba_adapters')
        return {row[1]: {'name': row[2], 'price': row[3]} for row in cursor.fetchall()}


def get_capacity_disks():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM capacity_disks')
        capacity_disks = {'ssd': {}, 'nvme': {}}
        for row in cursor.fetchall():
            disk_type = row[1]
            capacity = row[2]
            price = row[3]
            capacity_disks[disk_type][capacity] = {'price': price}
        return capacity_disks


def get_rams_filtered(ram_gen_filter):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rams WHERE ram_gen = ?", (ram_gen_filter,))

        return [
            {
                'ram_gen': row[1],
                'ram_size': row[2],
                'price': row[3]
            }
            for row in cursor.fetchall()
        ]

def update_cpu_price(cpu_name, new_price):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE cpus SET price = ? WHERE name = ?", (new_price, cpu_name))
        conn.commit()

def update_server_price(server_name, new_price):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE servers SET price = ? WHERE name = ?", (new_price, server_name))
        conn.commit()
# update_cpu_price('Intel Core i7-12700K', 350.00)
# update_server_price('Dell PowerEdge R740', 2000.00)



def main():
    print("Основные параметры:", get_parameters())
    print("Коэффициенты работ:", get_works_coefficient())
    print("Конфигурация RAID:", get_raid_config())
    print("Конфигурация RAID ГБ:", get_raids_data())
    print("ЦП", get_cpus_filtered())
    print("Servers", get_servers_filtered())
    print(f'ESXI: {get_esxi_disks()}')
    print("Cache Disc:", get_cache_disks())
    print("Network Card:", get_network_cards())
    print("HBA Adapters:", get_hba_adapters())
    print("Capacity Disks:", get_capacity_disks())
    # print("RAM Modules:", get_rams_filtered())


if __name__ == "__main__":
    main()
