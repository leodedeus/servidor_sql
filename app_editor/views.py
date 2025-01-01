from django.shortcuts import render, redirect
from django.db import connection
from .models import Query
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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
@login_required  # Garante que o usuário esteja logado
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
    #query_history = Query.objects.all().order_by('-id')[:6]
    query_history = Query.objects.filter(user=request.user).order_by('-id')[:6]

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