from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from .forms import UserRegistrationForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso! Agora você pode fazer login.')
            return redirect('login')  # Redireciona para a tela de login
        else:
            messages.error(request, 'Erro ao criar o cadastro. Tente novamente!')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login(request):
    if request.method == 'POST':  # Verifica se o método da requisição é POST
        username = request.POST['username']  # Obtém o nome de usuário do formulário
        password = request.POST['password']  # Obtém a senha do formulário
        user = authenticate(request, username=username, password=password)  # Tenta autenticar o usuário
        
        if user is not None:  # Se o usuário foi autenticado com sucesso
            auth_login(request, user)  # Faz o login do usuário
            return redirect('http://127.0.0.1:8000/produto/')  # Redireciona para a página inicial ou outra página desejada
        else:
            error_message = "Usuário ou senha inválidos."  
            return render(request, 'registration/login.html', {'error_message': error_message})  # Renderiza a página de login com erro
    else:
        return render(request, 'registration/login.html')  # Renderiza a página de login se não for POST
    
def user_logout(request):
    logout(request)  # Desloga o usuário
    return redirect('login')  # Redireciona para a página de login

def get_user(request):

    return render(request, 'usuarios.html', {'active_page' : 'Usuarios'})

def user_data(request):
    usuarios = User.objects.all().values('id', 'username', 'email')
    usuarios_lista = list(usuarios)

    return JsonResponse({'usuarios': usuarios_lista})

@csrf_exempt
def user_delete(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse({'message': 'Usuário deletado com sucesso!'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado!'}, status=404)