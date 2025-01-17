import csv

with open('censo2022_demografia.csv', newline='', encoding='latin1') as csvfile:
    try:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            pass
    except csv.Error as e:
        print(f"Erro na linha {i + 1}: {e}")
