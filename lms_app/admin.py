from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Book, Category, Borrow
from import_export import resources

# تعريف الموارد لكل نموذج
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class BookResource(resources.ModelResource):
    class Meta:
        model = Book

class BorrowResource(resources.ModelResource):
    class Meta:
        model = Borrow

# تسجيل النماذج مع ميزات الاستيراد والتصدير
@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource



class BorrowAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrow_date', 'due_date', 'return_date', 'is_overdue')
    list_filter = ('borrow_date', 'due_date', 'return_date')
    search_fields = ('book__title', 'user__username')

admin.site.register(Borrow, BorrowAdmin)
