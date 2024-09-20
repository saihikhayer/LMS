from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
       path('admin-login/', views.admin_login, name='admin_login'),
    path('student-login/', views.student_login, name='student_login'),
    
    path('books/', views.books, name='books'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete_book'),
     path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('my-borrows/', views.borrow_list, name='borrow_list'),
      path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_book/', views.add_book, name='add_book'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('admin_view_borrowed_books/', views.admin_view_borrowed_books, name='admin_view_borrowed_books'),
     path('student_books/', views.student_books, name='student_books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
     path('student_view_borrowed_books/', views.student_view_borrowed_books, name='student_view_borrowed_books'),
        path('return_book/<int:borrow_id>/', views.return_book, name='return_book'),
         path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
           path('books_by_category/<int:category_id>/', views.books_by_category, name='books_by_category'),
           path('categories/<int:category_id>/', views.books_by_category, name='books_by_category'),
           path('books_by_category/', views.books_by_category, name='books_by_category'),
            path('admin/borrow-history/pdf/', views.generate_borrow_history_pdf, name='generate_borrow_history_pdf'),
            path('admin/logout/', auth_views.LogoutView.as_view(next_page='admin_login'), name='admin_logout'),
    
    # Student logout
       path('student/logout/', auth_views.LogoutView.as_view(next_page='student_login'), name='student_logout'),

]
