from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Admin login/logout
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='admin_login'), name='admin_logout'),

    # Student login/logout
    path('student-login/', views.student_login, name='student_login'),
    path('student/logout/', auth_views.LogoutView.as_view(next_page='student_login'), name='student_logout'),

    # Book management
    path('books/', views.books, name='books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('add_book/', views.add_book, name='add_book'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete_book'),

    # Borrow and return books
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('student_books/', views.student_books, name='student_books'),

    # User borrow lists
    path('my-borrows/', views.borrow_list, name='borrow_list'),

    # Dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    # Borrowed books views
    path('admin_view_borrowed_books/', views.admin_view_borrowed_books, name='admin_view_borrowed_books'),
    path('student_view_borrowed_books/', views.student_view_borrowed_books, name='student_view_borrowed_books'),

    # Category management
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('books_by_category/<int:category_id>/', views.books_by_category, name='books_by_category'),
    path('books_by_category/', views.books_by_category, name='books_by_category'),
]


