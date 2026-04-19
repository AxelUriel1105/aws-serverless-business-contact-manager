import csv
import os
import random
import string

def generate_random_name():
    first_names = ["Axel", "Ana", "Salvador", "Baila", "Fernando", "Uriel", "Guerra", "Morales", "Kahn", "Reyes"]
    last_names = ["Aparicio", "Castelan", "Gomez", "Lopez", "Perez", "Rodriguez", "Sanchez", "Ramirez", "Torres", "Flores"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_phone():
    return "".join(random.choices(string.digits, k=10))

def generate_random_email(name, index):
    clean_name = name.lower().replace(" ", ".")
    return f"{clean_name}.{index}@example.com"

def create_massive_csv(filename, total_rows):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    headers = ['name', 'phone', 'email']
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        
        for i in range(1, total_rows + 1):
            name = generate_random_name()
            row = {
                'name': name,
                'phone': generate_random_phone(),
                'email': generate_random_email(name, i)
            }
            writer.writerow(row)
            
            if i % 100000 == 0:
                print(f"Progreso: {i} registros generados...")

if __name__ == "__main__":
    target_path = os.path.join("csv_files", "contacts_1mln.csv")
    rows = 1000000
    
    print(f"Iniciando generación de {rows} registros en: {target_path}")
    create_massive_csv(target_path, rows)
    print("¡Archivo generado exitosamente!")