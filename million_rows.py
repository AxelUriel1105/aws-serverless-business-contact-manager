import csv, uuid, random
with open('csv_files/million_rows.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'phone', 'email'])
    for i in range(1000000):
        writer.writerow([f'Contact {i}', f'55{random.randint(10000000,99999999)}', f'contact{i}_{uuid.uuid4().hex[:8]}@test.com'])
print('Done')