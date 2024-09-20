from .models import Book , Category,Borrow
from django import forms

class CategoryForm(forms.ModelForm):
    class Meta :
        model = Category
        fields = ['name']
            


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'photo_book', 'photo_author', 'pages', 'total_copies', 'available_copies', 'status', 'category']

        widjet = {

        }




class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['book']  # يجب أن يتضمن الحقول المناسبة فقط
