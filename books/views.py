from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import BooksForm
from .models import Books
from django.contrib.auth.decorators import login_required

# Create your views here.

# Index Page
def index(request):

    books = Books.objects.all()
    books_index = books[:8]

    return render(request, 'index.html', {
        'books': books_index,
    })


# Account Creation
def signup(request):

    if request.method == 'GET':

        return render(request, 'login/signup.html', {
            'form': UserCreationForm
        })

    else:

        if request.POST['password1'] == request.POST['password2']:

            try:
                # Register User
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)

                return redirect('index')

            except IntegrityError:
                # Failed Register
                return render(request, 'login/signup.html', {
                    'form': UserCreationForm,
                    'error': 'Nombre de usuario ya existe'
                })

        return render(request, 'login/signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })


# Logout Account
@login_required
def signout(request):

    logout(request)
    return redirect('index')


# Login Account
def signin(request):

    if request.method == 'GET':

        return render(request, 'login/signin.html', {
            'form': AuthenticationForm
        })

    else:

        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'login/signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })

        else:

            login(request, user)
            return redirect('index')


@login_required
# Books Registration
def register_book(request):

    if request.method == 'GET':

        return render(request, "crudBooks/registerBook.html", {
            'form': BooksForm
        })

    else:

        try:
            form = BooksForm(request.POST) and Books(request.FILE)
            new_book = form.save(commit=False)
            new_book.save()

            return redirect('products')

        except:
            return render(request, 'crudBooks/registerBook.html', {
                'form': BooksForm,
                'error': 'Ingresa datos validos'
            })



def item(request, id):
    
    book = get_object_or_404(Books, pk = id)
    book_item = Books.objects.all()
    book_item_separate = book_item[:4]

    return render(request, "crudBooks/item.html", {
        'book': book,
        'book_item': book_item_separate
    })


@login_required
def update(request, id):

    if request.method == 'GET':

        book = get_object_or_404(Books, pk = id)
        form = BooksForm(instance=book)
        return render(request, "crudBooks/update.html", {
            'book': book,
            'form': form
        })
    
    else:

        try:
            book = get_object_or_404(Books, pk = id)
            form = BooksForm(request.POST, instance = book)
            form.save()

            return redirect('crudBooks/mod_book')
        
        except ValueError:

            return render(request, "crudBooks/update.html", {
                'book': book,
                'form': form,
                'error': "Error Updating"
            })


def delete(request, id):

    book = get_object_or_404(Books, pk = id)

    if request.method == 'POST':
        book.delete()

        return redirect('crudBooks/mod_book')


@login_required
def mod_book(request):

    books = Books.objects.all()

    return render(request, "crudBooks/mod_book.html", {
        'books': books
    })


def products(request):

    books = Books.objects.all()
    return render(request, "crudBooks/products.html", {
        'books': books
    })


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def shoppingCart(request):

    books = Books.objects.all()
    return render(request, "buy/shoppingCart.html", {
        'books': books
    })