from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        label="Quantity",
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={"class": "form-control", "size": "2"}),
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )
