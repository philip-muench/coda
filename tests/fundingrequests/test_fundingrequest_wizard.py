from typing import Any, cast

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from coda.apps.authors.dto import AuthorDto
from coda.apps.authors.models import Role
from coda.apps.fundingrequests.dto import CostDto, ExternalFundingDto
from coda.apps.institutions.models import Institution
from coda.apps.publications.dto import PublicationDto
from coda.apps.publications.forms import PublicationFormData
from coda.apps.users.models import User
from tests import test_orcid
from tests.fundingrequests import factory
from tests.fundingrequests.assertions import (
    assert_author_equal,
    assert_correct_funding_request,
    assert_cost_equal,
    assert_external_funding_equal,
    assert_publication_equal,
)
from tests.fundingrequests.test_fundingrequest_services import author_dto_from_request


@pytest.fixture(autouse=True)
@pytest.mark.django_db
def login(client: Client) -> None:
    client.force_login(User.objects.create_user(username="testuser"))


@pytest.mark.django_db
def test__completing_fundingrequest_wizard__creates_funding_request_and_shows_details(
    client: Client,
) -> None:
    author_dto = factory.valid_author_dto(factory.institution().pk)
    journal_pk = factory.journal().pk
    journal_post_data = {"journal": journal_pk}

    publication_dto = factory.publication_dto(journal_pk)
    publication_post_data = create_publication_post_data(publication_dto)
    funder = factory.funding_organization()
    external_funding = factory.external_funding_dto(funder.pk)
    cost_dto = factory.cost_dto()

    response = submit_wizard(
        client, author_dto, journal_post_data, publication_post_data, external_funding, cost_dto
    )

    funding_request = assert_correct_funding_request(
        author_dto, publication_dto, external_funding, cost_dto
    )
    assertRedirects(response, reverse("fundingrequests:detail", kwargs={"pk": funding_request.pk}))


@pytest.mark.django_db
def test__updating_fundingrequest_submitter__updates_funding_request_and_shows_details(
    client: Client,
) -> None:
    request = factory.fundingrequest()
    affiliation = Institution.objects.create(name="New Institution")

    new_author = AuthorDto(
        name="New Author",
        email="newauthor@mail.com",
        affiliation=affiliation.pk,
        orcid=test_orcid.LAUREL_HAAK,
        roles=[Role.CO_AUTHOR.name],
    )

    response = client.post(
        reverse("fundingrequests:update_submitter", kwargs={"pk": request.pk}),
        next() | new_author,
    )

    request.refresh_from_db()
    assert_author_equal(new_author, request.submitter)
    assertRedirects(response, reverse("fundingrequests:detail", kwargs={"pk": request.pk}))


@pytest.mark.django_db
def test__updating_fundingrequest_publication__updates_funding_request_and_shows_details(
    client: Client,
) -> None:
    request = factory.fundingrequest()
    new_journal = factory.journal()
    new_publication = factory.publication_dto(new_journal.pk)
    publication_post_data = create_publication_post_data(new_publication)

    _ = client.post(
        reverse("fundingrequests:update_publication", kwargs={"pk": request.pk}),
        next() | publication_post_data,
    )
    response = client.post(
        reverse("fundingrequests:update_publication", kwargs={"pk": request.pk}),
        next() | {"journal": new_journal.pk},
    )

    request.refresh_from_db()
    assert_publication_equal(new_publication, author_dto_from_request(request), request.publication)
    assertRedirects(response, reverse("fundingrequests:detail", kwargs={"pk": request.pk}))


@pytest.mark.django_db
def test__updating_fundingrequest_funding__updates_funding_request_and_shows_details(
    client: Client,
) -> None:
    request = factory.fundingrequest()
    funder = factory.funding_organization()
    external_funding = factory.external_funding_dto(funder.pk)
    cost_dto = factory.cost_dto()

    response = client.post(
        reverse("fundingrequests:update_funding", kwargs={"pk": request.pk}),
        next() | external_funding | cost_dto,
    )

    request.refresh_from_db()
    assert_cost_equal(cost_dto, request)
    assert_external_funding_equal(external_funding, request)
    assertRedirects(response, reverse("fundingrequests:detail", kwargs={"pk": request.pk}))


def next() -> dict[str, str]:
    return {"action": "next"}


def submit_wizard(
    client: Client,
    author: AuthorDto,
    journal: dict[str, int],
    publication_post_data: dict[str, Any],
    external_funding: ExternalFundingDto,
    cost: CostDto,
) -> HttpResponse:
    client.post(reverse("fundingrequests:create_wizard"), next() | author)
    client.post(reverse("fundingrequests:create_wizard"), next() | journal)
    client.post(reverse("fundingrequests:create_wizard"), next() | publication_post_data)
    return cast(
        HttpResponse,
        client.post(reverse("fundingrequests:create_wizard"), next() | external_funding | cost),
    )


def create_publication_post_data(publication: PublicationDto) -> dict[str, Any]:
    link_form_data: dict[str, list[str]] = {"link_type": [], "link_value": []}
    for link in publication["links"]:
        link_form_data["link_type"].append(str(link["link_type"]))
        link_form_data["link_value"].append(str(link["link_value"]))

    publication_form_data = PublicationFormData(
        title=publication["title"],
        open_access_type=publication["open_access_type"],
        publication_state=publication["publication_state"],
        publication_date=publication["publication_date"],
    )

    return {**publication_form_data, **link_form_data}
