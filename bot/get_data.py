import sqlite3
import json
from collections import defaultdict

# Подключение к базе данных
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Получение основных параметров
c.execute("SELECT param_name, param_value FROM parameters")
parameters = {row[0]: float(row[1]) for row in c.fetchall()}

# Получение коэффициентов работ
c.execute("SELECT service, hosts_8, hosts_16, hosts_24, hosts_32, hosts_64, hosts_96, hosts_128 FROM works_coefficient")
works_coefficient = {row[0]: list(row[1:]) for row in c.fetchall()}

# Получение конфигурации RAID
c.execute("SELECT raid_level, FTM, FTT, disk_usage_overhead FROM raid_config")
raid_config = {row[0]: {'FTM': row[1], 'FTT': row[2], 'disk_usage_overhead': row[3]} for row in c.fetchall()}

# Запрос на получение всех данных из базы данных
c.execute('SELECT raid_type, level, item_id, value_id, value FROM raids')

# Получаем все строки из результата запроса
rows = c.fetchall()

# Создаём структуру данных, которая будет хранить данные в исходном формате
raids_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

# Заполняем структуру данными
for raid_type, level, item_id, value_id, value in rows:
    raids_data[raid_type][level][item_id][value_id] = value

# Преобразуем структуру данных в обычный словарь
# Преобразуем в обычный словарь
raids_data = {raid_type: {level: dict(items) for level, items in levels.items()} for raid_type, levels in raids_data.items()}
raids_data = {raid_type: {level: {item_id: dict(values) for item_id, values in items.items()} for level, items in levels.items()} for raid_type, levels in raids_data.items()}

# Выполнение запроса для получения всех данных из таблицы
c.execute('SELECT * FROM cpus')

# Извлечение всех строк из результата запроса
rows = c.fetchall()

# Преобразуем данные обратно в список словарей
cpus_from_db = []
for row in rows:
    cpu = {
        'manufacturer': row[1],
        'name': row[2],
        'cores_quantity': row[3],
        'cores_frequency': row[4],
        'price': row[5],
        'socket': row[6],
        'ram_gen': row[7],
    }
    cpus_from_db.append(cpu)

# Выполнение запроса для получения всех данных из таблицы
c.execute('SELECT * FROM servers')

# Извлечение всех строк из результата запроса
rows = c.fetchall()

# Преобразуем данные обратно в список словарей
servers_from_db = []
for row in rows:
    server = {
        'name': row[1],
        'cpu_vendor': row[2],
        'socket': row[3],
        'max_ram': row[4],
        'ram_gen': row[5],
        'max_disks_qty': row[6],
        'price': row[7],
    }
    servers_from_db.append(server)


# Извлечение данных о дисках ESXi
c.execute('SELECT * FROM esxi_disks')
esxi_disks = {}
for row in c.fetchall():
    disk_type = row[1]  # disk_type
    disk_size = row[2]  # disk_size
    price = row[3]      # price
    esxi_disks[disk_type] = {'type': disk_size, 'price': price}

# Извлечение данных о кэш-дисках
c.execute('SELECT * FROM cache_disks')
cache_disc = {}
for row in c.fetchall():
    disk_type = row[1]  # disk_type
    size = row[2]       # size
    vendor = row[3]     # vendor
    price = row[4]      # price
    cache_disc = {'type': disk_type, 'size': size, 'vendor': vendor, 'price': price}

# Извлечение данных о сетевых картах
c.execute('SELECT * FROM network_cards')
network_card = {}
for row in c.fetchall():
    name = row[1]   # name
    price = row[2]  # price
    network_card = {'name': name, 'price': price}

# Извлечение данных о HBA адаптерах
c.execute('SELECT * FROM hba_adapters')
hba_adapters = {}
for row in c.fetchall():
    spec = row[1]   # spec
    name = row[2]   # name
    price = row[3]  # price
    hba_adapters[spec] = {'name': name, 'price': price}

# Извлечение данных из таблицы capacity_disks
c.execute('SELECT * FROM capacity_disks')
capacity_disks = {'ssd': {}, 'nvme': {}}

# Заполнение словаря данными из базы
for row in c.fetchall():
    disk_type = row[1]  # disk_type
    disk_capacity = row[2]  # disk_capacity
    name = row[3]  # name
    price = row[4]  # price
    capacity_disks[disk_type][disk_capacity] = {'name': name, 'price': price}

# Извлечение данных из таблицы rams
c.execute('SELECT * FROM rams')
rams = []

# Заполнение списка данными из базы
for row in c.fetchall():
    ram = {
        'ram_gen': row[1],  # ram_gen
        'ram_size': row[2],  # ram_size
        'price': row[3]  # price
    }
    rams.append(ram)

# Закрытие соединения
conn.close()

# Вывод восстановленных данных
print("Основные параметры:")
print(parameters)
print("\nКоэффициенты работ:")
print(works_coefficient)
print("\nКонфигурация RAID:")
print(raid_config)
print("\nКонфигурация RAID ГБ:")
print(raids_data)
print("ЦП")
print(cpus_from_db)
print("Servers")
print(servers_from_db)
print(f'{esxi_disks}')
print("Cache Disc:", cache_disc)
print("Network Card:", network_card)
print("HBA Adapters:", hba_adapters)
print("Capacity Disks:", capacity_disks)
print("RAM Modules:", rams)


