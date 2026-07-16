from django import forms

from academics.models import SchoolClass

from .models import FeeStructure, Payment


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ["fee_type", "school_class", "amount"]
        widgets = {
            "fee_type": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Tuition Fee"}),
            "school_class": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }
        labels = {"school_class": "Class"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["school_class"].required = False
        # Group by Stream so the dropdown always reflects Class Setup live,
        # instead of one flat unsorted list of every class ever created.
        self.fields["school_class"].choices = [("", "All Classes")] + [
            (stream_label, [(c.id, str(c)) for c in stream_classes])
            for stream_label, stream_classes in SchoolClass.grouped_by_stream()
        ]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["amount", "date", "mode", "status"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "mode": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {"amount": "Installment Amount (₹)"}
        help_texts = {"amount": "Enter the amount for this specific installment."}
