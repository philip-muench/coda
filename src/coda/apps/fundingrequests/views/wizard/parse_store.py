import datetime

from coda.apps.publications.dto import LinkDto, PublicationDto
from coda.apps.publications.forms import PublicationFormData
from coda.apps.wizard import Store


def publication_dto_from(store: Store) -> PublicationDto:
    publication_form_data: PublicationFormData = store["publication"]
    link_form_data: list[LinkDto] = store["links"]
    journal = store["journal"]
    publication_dto = PublicationDto(
        title=publication_form_data["title"],
        authors=store["authors"],
        license=publication_form_data["license"],
        open_access_type=publication_form_data["open_access_type"],
        publication_state=publication_form_data["publication_state"],
        publication_date=_parse_date(publication_form_data),
        links=link_form_data,
        journal=int(journal),
    )

    return publication_dto


def _parse_date(publication_form_data: PublicationFormData) -> datetime.date | None:
    maybe_date = publication_form_data["publication_date"]
    return datetime.date.fromisoformat(maybe_date) if maybe_date else None
