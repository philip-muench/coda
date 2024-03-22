from typing import Any, cast

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from coda.apps.authors.dto import AuthorDto
from coda.apps.fundingrequests.dto import FundingDto
from coda.apps.publications.dto import LinkDto, PublicationDto
from coda.apps.publications.forms import PublicationFormData
from coda.apps.publications.models import LinkType
from coda.apps.users.models import User
from tests.fundingrequests import factory
from tests.fundingrequests.assertions import assert_correct_funding_request


@pytest.fixture(autouse=True)
@pytest.mark.django_db
def login(client: Client) -> None:
    client.force_login(User.objects.create_user(username="testuser"))


@pytest.mark.django_db
def test__completing_fundingrequest_wizard__creates_funding_request_and_shows_details__2(
    client: Client,
) -> None:
    author_dto = factory.valid_author_dto(factory.institution().pk)
    journal_pk = factory.journal().pk
    journal_post_data = {"journal": journal_pk}

    links = create_link_dtos()
    publication_dto = factory.publication_dto(journal_pk, links=links)
    publication_post_data = create_publication_post_data(links, publication_dto)
    funding_dto = factory.funding_dto()

    response = submit_wizard_new(
        client, author_dto, journal_post_data, publication_post_data, funding_dto
    )

    funding_request = assert_correct_funding_request(author_dto, publication_dto, funding_dto)
    assertRedirects(response, reverse("fundingrequests:detail", kwargs={"pk": funding_request.pk}))


def submit_wizard_new(
    client: Client,
    author: AuthorDto,
    journal: dict[str, int],
    publication_post_data: dict[str, Any],
    funding: FundingDto,
) -> HttpResponse:
    next = {"action": "next"}
    client.post(reverse("fundingrequests:create_wizard"), next | author)
    client.post(reverse("fundingrequests:create_wizard"), next | journal)
    client.post(reverse("fundingrequests:create_wizard"), next | publication_post_data)
    return cast(HttpResponse, client.post(reverse("fundingrequests:create_wizard"), next | funding))


def submit_wizard(
    client: Client,
    author: AuthorDto,
    journal: dict[str, int],
    publication_post_data: dict[str, Any],
    funding: FundingDto,
) -> HttpResponse:
    client.post(reverse("fundingrequests:create_submitter"), author)
    client.post(reverse("fundingrequests:create_journal"), journal)
    client.post(reverse("fundingrequests:create_publication"), publication_post_data)
    return cast(HttpResponse, client.post(reverse("fundingrequests:create_funding"), funding))


def create_link_dtos() -> list[LinkDto]:
    doi = LinkType.objects.create(name="DOI")
    url = LinkType.objects.create(name="URL")

    doi_link = LinkDto(link_type=int(doi.pk), link_value="10.1234/5678")
    url_link = LinkDto(link_type=int(url.pk), link_value="https://example.com")
    return [doi_link, url_link]


def create_publication_post_data(
    links: list[LinkDto], publication: PublicationDto
) -> dict[str, Any]:
    link_form_data: dict[str, list[str]] = {"link_type": [], "link_value": []}
    for link in links:
        link_form_data["link_type"].append(str(link["link_type"]))
        link_form_data["link_value"].append(str(link["link_value"]))

    publication_form_data = PublicationFormData(
        title=publication["title"],
        publication_state=publication["publication_state"],
        publication_date=publication["publication_date"],
    )

    return {**publication_form_data, **link_form_data}
