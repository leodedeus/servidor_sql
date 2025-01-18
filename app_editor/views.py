from django.shortcuts import render, redirect
from django.db import connection
from .models import Query
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
import re

def home(request):
    return render(request, 'app_editor/home.html')  # Renderiza a tela inicial

# View para logout
def logout_view(request):
    logout(request)  # Realiza o logout
    return redirect('home')  # Redireciona para a tela inicial
'''
@login_required #para garantir que o usuário esteja logado
def sql_editor(request):
    result = None
    error = None

    if request.method == 'POST':
        sql_command = request.POST.get('sql_command')  # Pega o comando enviado pelo formulário

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                if sql_command.strip().lower().startswith('select'):
                    result = cursor.fetchall()  # Retorna os dados para exibir
                    columns = [col[0] for col in cursor.description]
                else:
                    result = f"Comando executado com sucesso: {cursor.rowcount} linhas afetadas."
                    columns = None

            # Salva no histórico com status de sucesso
            Query.objects.create(sql_command=sql_command, result="success")
        except Exception as e:
            # Salva no histórico com status de erro
            error = str(e)
            Query.objects.create(sql_command=sql_command, result=f"Erro: {error}")

    # Histórico de comandos
    query_history = Query.objects.all().order_by('-id')[:6]

    # Adicionar um indicador de sucesso ou erro para o template
    history_with_status = [
        {
            'command': query.sql_command,
            'status': 'success' if query.result == "success" else 'error',
            'message': query.result,
        }
        for query in query_history
    ]

    return render(request, 'app_editor/sql_editor.html', {
        'result': result,
        'columns': columns if result and columns else None,
        'error': error,
        'query_history': history_with_status,  # Passa a nova lista
    })
'''
# Função para verificar comandos e tabelas proibidos
def is_command_forbidden(sql_command, forbidden_tables):
    # Lista de comandos proibidos
    forbidden_commands = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER"]

    # Extrai o tipo de comando SQL
    sql_command_clean = sql_command.strip().upper()
    command_type = sql_command_clean.split()[0]

    # Se o comando estiver na lista de proibidos
    if command_type in forbidden_commands:
        # Percorre as tabelas proibidas e verifica sua presença no comando
        for table in forbidden_tables:
            # Cria um padrão regex para encontrar o nome da tabela de forma precisa
            pattern = r'\b' + re.escape(table) + r'\b'
            if re.search(pattern, sql_command_clean, re.IGNORECASE):
                return True
    return False

@login_required  # Garante que o usuário esteja logado
def sql_editor(request):
    result = None
    error = None
    query_columns = None  # Para armazenar as colunas da consulta executada

    # Define as tabelas que não podem ser alteradas
    forbidden_tables = ["test", "censo2022_basico", "censo2022_demografia", "querys"]

    if request.method == 'POST':
        sql_command = request.POST.get('sql_command')  # Pega o comando enviado pelo formulário

        # Verificar se o comando SQL é proibido
        if is_command_forbidden(sql_command, forbidden_tables):
            error = "Você não tem permissão para executar este comando SQL ou alterar tabelas protegidas."
            Query.objects.create(
                user=request.user,
                sql_command=sql_command,
                result=f"Erro: {error}"
            )
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql_command)
                    if sql_command.strip().lower().startswith('select'):
                        result = cursor.fetchall()  # Retorna os dados para exibir
                        query_columns = [col[0] for col in cursor.description]
                    else:
                        result = f"Comando executado com sucesso: {cursor.rowcount} linhas afetadas."
                        query_columns = None

                # Salva no histórico com status de sucesso, associando o usuário logado
                Query.objects.create(
                    user=request.user,  # Adiciona o usuário logado
                    sql_command=sql_command,
                    result="success"
                )
            except Exception as e:
                # Salva no histórico com status de erro, associando o usuário logado
                error = str(e)
                Query.objects.create(
                    user=request.user,  # Adiciona o usuário logado
                    sql_command=sql_command,
                    result=f"Erro: {error}"
                )

    # Histórico de comandos
    query_history = Query.objects.filter(user=request.user).order_by('-id')[:10]

    # Adicionar um indicador de sucesso ou erro para o template
    history_with_status = [
        {
            'command': query.sql_command,
            'status': 'success' if query.result == "success" else 'error',
            'message': query.result,
        }
        for query in query_history
    ]

    tables_info = {}

    # Query para listar as tabelas no SQLite
    '''
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'django_%' AND name NOT LIKE 'auth_%' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
        tables = cursor.fetchall()

        # Para cada tabela, buscar as colunas
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            table_columns = [row[1] for row in cursor.fetchall()]  # O nome da coluna está na segunda posição
            tables_info[table_name] = table_columns
    '''
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'django_%' AND name NOT LIKE 'auth_%' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'querys' ORDER BY name;")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            columns_info = cursor.fetchall()  # Retorna todas as informações da tabela

            # Para chaves estrangeiras
            cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
            foreign_keys = cursor.fetchall()
            foreign_key_columns = {fk[3] for fk in foreign_keys}  # Colunas FK

            # Construir a lista de colunas com tipos e chaves
            columns = []
            for column in columns_info:
                column_name = column[1]
                column_type = column[2]
                is_pk = "PK" if column[5] == 1 else ""  # Verifica se é chave primária
                is_fk = "FK" if column_name in foreign_key_columns else ""  # Verifica se é chave estrangeira
                key_info = f"({column_type}) {is_pk} {is_fk}".strip()  # Monta o texto com tipo e chaves
                columns.append(f"{column_name} {key_info}")

            tables_info[table_name] = columns

    return render(request, 'app_editor/sql_editor.html', {
        'result': result,
        'columns': query_columns if result and query_columns else None,  # Use as colunas da consulta
        'error': error,
        'query_history': history_with_status,  # Passa a nova lista
        'tables_info': tables_info,  # Informações das tabelas
    })
'''
@login_required
def list_tables(request):
    tables_info = {}

    # Query para listar as tabelas no SQLite
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()

        # Para cada tabela, buscar as colunas
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            columns = [row[1] for row in cursor.fetchall()]  # O nome da coluna está na segunda posição
            tables_info[table_name] = columns

    # Verificando o conteúdo de tables_info
    print(tables_info)  # Adiciona esta linha para verificar o conteúdo

    # Renderizar o template com as tabelas e colunas
    return render(request, 'app_editor/sql_editor.html', {
        'tables_info': tables_info,
    })
'''