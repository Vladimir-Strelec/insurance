from django import forms
from .models import InsuranceMainCategory, InsuranceSubCategory, InsuranceProduct


class MainCategoryForm(forms.Form):
    main_category = forms.ModelChoiceField(
        queryset=InsuranceMainCategory.objects.all(),
        label="Основная категория",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SubCategoryForm(forms.Form):
    subcategory = forms.ModelChoiceField(
        queryset=InsuranceSubCategory.objects.none(),
        label="Подкатегория",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        main_category = kwargs.pop('main_category', None)
        super().__init__(*args, **kwargs)
        if main_category:
            self.fields['subcategory'].queryset = InsuranceSubCategory.objects.filter(main_category=main_category)


class ProductForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=InsuranceProduct.objects.none(),
        label="Продукт",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        subcategory = kwargs.pop('subcategory', None)
        super().__init__(*args, **kwargs)
        if subcategory:
            self.fields['product'].queryset = InsuranceProduct.objects.filter(subcategory=subcategory)

