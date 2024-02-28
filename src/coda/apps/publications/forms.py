from typing import TypedDict

from django import forms

from coda.apps.publications.dto import LinkDto
from coda.apps.publications.models import LinkType, Publication


class PublicationFormData(TypedDict):
    title: str
    publication_state: str
    publication_date: str


class PublicationForm(forms.Form):
    title = forms.CharField()
    publication_state = forms.ChoiceField(
        choices=Publication.STATES, initial=Publication.State.SUBMITTED
    )
    publication_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def get_form_data(self) -> PublicationFormData:
        return PublicationFormData(
            title=self.cleaned_data["title"],
            publication_state=self.cleaned_data["publication_state"],
            publication_date=str(self.cleaned_data["publication_date"]),
        )


class LinkForm(forms.Form):
    link_type = forms.ModelChoiceField(queryset=LinkType.objects.all())
    link_value = forms.CharField()

    def get_form_data(self) -> LinkDto:
        return LinkDto(
            link_type=self.cleaned_data["link_type"].pk,
            link_value=self.cleaned_data["link_value"],
        )
