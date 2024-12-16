from django.shortcuts import render
from django.db import connection
from .models import Query

'''
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
                else:
                    result = f"Comando executado com sucesso: {cursor.rowcount} linhas afetadas."
                
            # Salva a consulta no banco de dados
            Query.objects.create(sql_command=sql_command, result=str(result))

        except Exception as e:
            error = str(e)  # Captura qualquer erro de execução

    return render(request, 'app_editor/sql_editor.html', {
        'result': result,
        'error': error,
    })
'''

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
                    columns = [col[0] for col in cursor.description]  # Obtém os nomes das colunas
                else:
                    result = f"Comando executado com sucesso: {cursor.rowcount} linhas afetadas."
                    columns = None

            # Salva o comando com resultado vazio (sem erro)
            Query.objects.create(sql_command=sql_command, result="")

        except Exception as e:
            # Captura o erro e salva no banco
            error = str(e)
            Query.objects.create(sql_command=sql_command, result=error)

    # Recupera os últimos comandos do banco de dados
    query_history = Query.objects.order_by('-id')[:10]

    return render(request, 'app_editor/sql_editor.html', {
        'result': result,
        'error': error,
        'columns': locals().get('columns'),
        'query_history': query_history,
    })

