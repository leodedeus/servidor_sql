import csv

# Caminho do arquivo CSV
csv_file = 'votacao_partidos.csv'

# Abrir o arquivo CSV com a codificação 'latin1'
with open(csv_file, encoding='latin1') as f:
    reader = csv.reader(f, delimiter=';')
    headers = next(reader)  # Lê a primeira linha, que são os cabeçalhos
    
    # Gerar o comando SQL para criação da tabela
    create_table_sql = f"CREATE TABLE votacao_partidos ({', '.join([f'{header} TEXT' for header in headers])});"
    print(create_table_sql)
