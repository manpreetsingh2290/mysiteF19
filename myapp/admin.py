from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review


def make_available(modeladmin, request, queryset):
    #print(queryset)
    for book in queryset:
        book.price = book.price+10
        #print(book.price)
        book.save()
    return


make_available.short_description = 'Add $10 to the current price'


class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ('title', 'category', 'price')
    actions = [make_available]


class OrderAdmin(admin.ModelAdmin):
    fields = ['books', ('member', 'order_type', 'order_date')]
    list_display = ('id', 'member', 'order_type', 'order_date', 'total_items')


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'city')


# Register your models here.

admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Member)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
