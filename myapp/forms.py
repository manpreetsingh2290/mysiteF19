from django import forms
from myapp.models import Order, Review


class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Science&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    name = forms.CharField(label="Your Name", max_length=100, required=False)
    category = forms.ChoiceField(label="Select a Category", widget=forms.RadioSelect, choices=CATEGORY_CHOICES,
                                 required=False)
    max_price = forms.IntegerField(label="Maximum Price", min_value=0)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'member': u'Member name', }


class ReviewForm(forms.ModelForm):
    class Meta:

        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {'reviewer': forms.EmailInput(),
                   'book': forms.RadioSelect(),
                   'rating': forms.NumberInput(),
                   'comments': forms.Textarea()
                   }
        labels = {'reviewer': u"Please enter a valid Email Id", 'rating': u"Rating: An integer between 1 (worst) and 5 (best)"}
