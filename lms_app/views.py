from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Category, Book, Borrow
from .forms import BookForm, CategoryForm, BorrowForm

# Index view to display all books and categories

#def index(request):
    #if request.method == 'POST':
      #  add_book = BookForm(request.POST, request.FILES)
       # if add_book.is_valid():
       #     add_book.save()

       # add_cat = CategoryForm(request.POST)
       # if add_cat.is_valid():
       #     add_cat.save()

   # context = {
      #  'category': Category.objects.all(),
      #  'books': Book.objects.all(),
       # 'form': BookForm(),
       # 'catform': CategoryForm(),
       # 'allbooks': Book.objects.filter(active=True).count,
   # }

   # return render(request, 'pages/index.html', context)

# View to search and list books
# views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book, Category

# views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book, Category

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book, Category

def books(request):
    search = Book.objects.all()
    
    if 'search_name' in request.GET:
        title = request.GET['search_name']
        if title:
            search = search.filter(title__icontains=title)

    # Pagination logic: Display 12 books per page
    paginator = Paginator(search, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': Category.objects.all(),
        'books': page_obj,
        'username': request.user.username 
    }
    return render(request, 'pages/books.html', context)




# View to update a book
@login_required
def update(request, id):
    book_id = Book.objects.get(id=id)
    if request.method == 'POST':
        book_save = BookForm(request.POST, request.FILES, instance=book_id)
        if book_save.is_valid():
            book_save.save()
            return redirect('books')
    else:
        book_save = BookForm(instance=book_id)

    context = {
        'form': book_save,
    }

    return render(request, 'pages/update.html', context)

# View to delete a book


@login_required
def delete(request, id):
    book_delete = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        book_delete.delete()
        return redirect('books')

    return render(request, 'pages/delete_book.html')

# View to handle borrowing a book

# View to return a borrowed book

# View to list borrowed books
@login_required
def borrow_list(request):
    borrowed_books = Borrow.objects.filter(user=request.user)

    return render(request, 'pages/borrow_list.html', {'borrowed_books': borrowed_books})







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




from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Borrow  # Replace with your actual model

@login_required
def admin_view_borrowed_books(request):
    # Books that are currently borrowed (i.e., no return date)
    current_borrows = Borrow.objects.filter(return_date__isnull=True)
    
    # Books that have been borrowed and returned (i.e., has a return date)
    borrow_history = Borrow.objects.filter(return_date__isnull=False).order_by('-borrow_date')

    context = {
        'current_borrows': current_borrows,
        'borrow_history': borrow_history
    }

    return render(request, 'pages/admin_view_borrowed_books.html', context)





from django.core.paginator import Paginator

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book, Category
@login_required
def student_books(request):
    # Get all available books
    search = Book.objects.filter(available_copies__gt=0)

    # Handle search functionality
    title = request.GET.get('search_name', '')
    if title:
        search = search.filter(title__icontains=title)

    # Fetch all categories
    categories = Category.objects.all()

    # Dictionary to hold paginated books by category
    books_by_categories = {}

    for category in categories:
        # Get books within this category
        books_in_category = search.filter(category=category)
        
        # Paginate the books in each category
        paginator = Paginator(books_in_category, 2)  # Show 2 books per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Add paginated books to the dictionary
        books_by_categories[category] = page_obj

    # Render the template with the context
    return render(request, 'student_books.html', {
        'books_by_categories': books_by_categories,
        'search_name': title,  # Return the search query to the template for form retention
    })

    








@login_required
def book_detail(request, book_id):
    # Get the book based on the provided ID
    book = get_object_or_404(Book, id=book_id)
    
    return render(request, 'pages/book_detail.html', {'book': book})








from django.db.models import Count
from .models import Book, Borrow, Category
@login_required
def admin_dashboard(request):
    total_books = Book.objects.count()
    total_categories = Category.objects.count()
    total_borrowed_books = Borrow.objects.count()

    # Books borrowed per category
    borrowed_books_per_category = (
        Borrow.objects.values('book__category__name')
        .annotate(count=Count('book__category'))
        .order_by('-count')
    )

    # Most borrowed books
    most_borrowed_books = (
        Borrow.objects.values('book__title')
        .annotate(count=Count('book'))
        .order_by('-count')[:5]
    )

    context = {
        'total_books': total_books,
        'total_categories': total_categories,
        'total_borrowed_books': total_borrowed_books,
        'borrowed_books_per_category': borrowed_books_per_category,
        'most_borrowed_books': most_borrowed_books,
    }
    return render(request, 'admin_dashboard.html', context)





# lms_app/views.py



# lms_app/views.py

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Book, Borrow

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Check if there are available copies
    if book.available_copies > 0:
        if request.method == 'POST':
            borrow = Borrow(
                user=request.user,
                book=book,
                borrow_date=timezone.now(),
                due_date=timezone.now() + timezone.timedelta(days=14)  # Example: 2 weeks borrow period
            )
            borrow.save()
            
            # Decrease the number of available copies
            book.available_copies -= 1
            book.save()

            return redirect('student_view_borrowed_books')

        return render(request, 'pages/borrow_book.html', {'book': book})
    else:
        return render(request, 'pages/borrow_book.html', {'book': book, 'error': 'No copies available'})







@login_required
def student_view_borrowed_books(request):
    borrowed_books = Borrow.objects.filter(user=request.user, return_date__isnull=True)
    return render(request, 'pages/student_view_borrowed_books.html', {'borrowed_books': borrowed_books})














# views.py
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Borrow, Book

@login_required
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)
    
    if request.method == 'POST':
        # Mark the book as returned
        borrow.return_date = timezone.now()
        borrow.book.available_copies += 1  # Increment available copies
        borrow.book.status = 'available' if borrow.book.available_copies > 0 else 'rental'
        borrow.book.save()
        borrow.save()
        return redirect('student_view_borrowed_books')  # Redirect to the student's list of borrowed books

    return render(request, 'pages/return_book.html', {'borrow': borrow})




from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Book, Borrow
from django.utils import timezone

@login_required
def student_dashboard(request):
    student = request.user
    # Borrowed books that are not yet returned
    currently_borrowed_books = Borrow.objects.filter(user=student, return_date__isnull=True)
    # Only include returned books in the borrow history
    borrow_history = Borrow.objects.filter(user=student, return_date__isnull=False)
    # Overdue books: due_date is in the past and return_date is still null
    overdue_books = Borrow.objects.filter(user=student, due_date__lt=timezone.now(), return_date__isnull=True)
    
    context = {
        'student': student,
        'borrowed_books': currently_borrowed_books,
        'borrow_history': borrow_history,
        'overdue_books': overdue_books,
    }
    return render(request, 'pages/student_dashboard.html', context)


from django.shortcuts import render
from .models import Book, Category
@login_required
def books_by_category(request):
    categories = Category.objects.all()  # Get all categories
    books = Book.objects.filter(available_copies__gt=0)  # Get available books

    # Create a dictionary to hold categories and their associated books
    books_by_categories = {}
    for category in categories:
        books_by_categories[category] = books.filter(category=category)

    return render(request, 'books_by_category.html', {
        'books_by_categories': books_by_categories
    })



from django.shortcuts import render
from .models import Book, Category

def home(request):
    # Get recently added books (e.g., last 10 books added)
    recent_books = Book.objects.order_by('-id')[:10]
    
    # Get all book categories
    categories = Category.objects.all()
    
    return render(request, 'home.html', {
        'recent_books': recent_books,
        'categories': categories,
    })










from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')  # Replace with your admin dashboard URL
        else:
            messages.error(request, 'Invalid credentials or not an admin.')
    return render(request, 'admin_login.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('student_dashboard')  # Replace with your student dashboard URL
        else:
            messages.error(request, 'Invalid credentials or not a student.')
    return render(request, 'student_login.html')















# views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book

def book_list(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 12)  # Show 12 books per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'book.html', {'page_obj': page_obj})


# views.py
