"""
Forms for the Skills app.

A ModelForm is a shortcut: it inspects the Skill model and builds matching
HTML form fields for us. We choose which fields to expose (NEVER include
`owner` — we set that ourselves in the view to prevent users impersonating
each other) and add a small clean() rule for price/is_free consistency.
"""
from django import forms
from .models import Skill


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        # Fields the user is allowed to edit. `owner` and `created_at` are
        # deliberately excluded — they are set by the system, not the user.
        fields = [
            'title',
            'description',
            'category',
            'is_free',
            'price',
            'contact_preference',
            'is_available',
        ]
        # Tweak a couple of widgets for nicer UX. Bootstrap classes get
        # added in the template via |add_class or by hand.
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        """Cross-field validation: price and is_free must agree."""
        cleaned = super().clean()
        is_free = cleaned.get('is_free')
        price = cleaned.get('price')

        if not is_free and price in (None, ''):
            # If they didn't tick "free" they need to give a price.
            self.add_error('price', 'Enter a price, or tick "Is free".')

        if is_free and price not in (None, ''):
            # If they ticked free, ignore any price they typed.
            cleaned['price'] = None

        return cleaned
