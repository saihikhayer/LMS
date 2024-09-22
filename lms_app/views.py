from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from datetime import timedelta
from .models import Category, Book, Borrow
from .forms import BookForm, CategoryForm, BorrowForm

# Index view to display all books and categories
def books(request):
    search = Book.objects.all()

    if 'search_name' in request.GET:
        title = request.GET['search_name']
        if title:
            search = search.filter(title__icontains=title)

    paginator = Paginator(search, 12)  # Display 12 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': Category.objects.all(),
        'books': page_obj,
        'username': request.user.username 
    }
    return render(request, 'pages/books.html', context)

# Update book view
@login_required
def update(request, id):
    book_instance = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm(instance=book_instance)

    context = {'form': form}
    return render(request, 'pages/update.html', context)

# Delete book view
@login_required
def delete (request, id):
    book_to_delete = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        book_to_delete.delete()
        return redirect('books')

    return render(request, 'pages/delete_book.html')

# View borrowed books (student)
@login_required
def borrow_list(request):
    borrowed_books = Borrow.objects.filter(user=request.user)
    return render(request, 'pages/borrow_list.html', {'borrowed_books': borrowed_books})

# Add book view (admin)
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

# Manage categories view (admin)
@login_required
def manage_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm()

    categories = Category.objects.all()
    return render(request, 'manage_categories.html', {'form': form, 'categories': categories})

# View borrowed books (admin)
@login_required
def admin_view_borrowed_books(request):
    current_borrows = Borrow.objects.filter(return_date__isnull=True)
    borrow_history = Borrow.objects.filter(return_date__isnull=False).order_by('-borrow_date')

    context = {
        'current_borrows': current_borrows,
        'borrow_history': borrow_history
    }
    return render(request, 'pages/admin_view_borrowed_books.html', context)

# Student books view with category and pagination
@login_required
def student_books(request):
    search = Book.objects.filter(available_copies__gt=0)
    title = request.GET.get('search_name', '')
    if title:
        search = search.filter(title__icontains=title)

    categories = Category.objects.all()
    books_by_categories = {}

    for category in categories:
        books_in_category = search.filter(category=category)
        paginator = Paginator(books_in_category, 2)  # 2 books per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        books_by_categories[category] = page_obj

    return render(request, 'student_books.html', {
        'books_by_categories': books_by_categories,
        'search_name': title
    })

# Book detail view
@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'pages/book_detail.html', {'book': book})

# Admin dashboard
@login_required
def admin_dashboard(request):
    total_books = Book.objects.count()
    total_categories = Category.objects.count()
    total_borrowed_books = Borrow.objects.count()
    current_borrows = Borrow.objects.filter(return_date__isnull=True).count()

    borrowed_books_per_category = Borrow.objects.values('book__category__name').annotate(count=Count('book__category')).order_by('-count')
    most_borrowed_books = Borrow.objects.values('book__title').annotate(count=Count('book')).order_by('-count')[:5]

    context = {
        'total_books': total_books,
        'current_borrows': current_borrows,
        'total_categories': total_categories,
        'total_borrowed_books': total_borrowed_books,
        'borrowed_books_per_category': borrowed_books_per_category,
        'most_borrowed_books': most_borrowed_books,
    }
    return render(request, 'admin_dashboard.html', context)

# Borrow book view
@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.available_copies > 0:
        if request.method == 'POST':
            borrow = Borrow(
                user=request.user,
                book=book,
                borrow_date=timezone.now(),
                due_date=timezone.now() + timedelta(days=14)
            )
            borrow.save()
            book.available_copies -= 1
            book.save()
            return redirect('student_view_borrowed_books')

        return render(request, 'pages/borrow_book.html', {'book': book})
    else:
        return render(request, 'pages/borrow_book.html', {'book': book, 'error': 'No copies available'})

# Return book view
@login_required
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)

    if request.method == 'POST':
        borrow.return_date = timezone.now()
        borrow.book.available_copies += 1
        borrow.book.status = 'available' if borrow.book.available_copies > 0 else 'rental'
        borrow.book.save()
        borrow.save()
        return redirect('student_view_borrowed_books')

    return render(request, 'pages/return_book.html', {'borrow': borrow})

# Student dashboard view
@login_required
def student_dashboard(request):
    student = request.user
    currently_borrowed_books = Borrow.objects.filter(user=student, return_date__isnull=True)
    borrow_history = Borrow.objects.filter(user=student, return_date__isnull=False)
    overdue_books = Borrow.objects.filter(user=student, due_date__lt=timezone.now(), return_date__isnull=True)

    context = {
        'student': student,
        'borrowed_books': currently_borrowed_books,
        'borrow_history': borrow_history,
        'overdue_books': overdue_books,
    }
    return render(request, 'pages/student_dashboard.html', context)

# Books by category
@login_required
def books_by_category(request):
    categories = Category.objects.all()
    books = Book.objects.filter(available_copies__gt=0)
    books_by_categories = {category: books.filter(category=category) for category in categories}
    return render(request, 'books_by_category.html', {'books_by_categories': books_by_categories})

# Homepage
def home(request):
    recent_books = Book.objects.order_by('-id')[:10]
    categories = Category.objects.all()
    return render(request, 'home.html', {'recent_books': recent_books, 'categories': categories})

# Admin login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin.')
    return render(request, 'admin_login.html')

# Student login view
def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a student.')
    return render(request, 'student_login.html')

# Book list with pagination
def book_list(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'book.html', {'page_obj': page_obj})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Borrow

@login_required
def student_view_borrowed_books(request):
    # الحصول على الكتب المستعارة من قبل الطالب الحالي والتي لم تتم إعادتها بعد
    borrowed_books = Borrow.objects.filter(user=request.user, return_date__isnull=True)
    
    return render(request, 'pages/student_view_borrowed_books.html', {'borrowed_books': borrowed_books})
