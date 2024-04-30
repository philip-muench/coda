from typing import cast

import pytest

from coda.apps.authors.dto import author_dto_from_model
from coda.apps.authors.models import Author
from coda.apps.journals.models import Journal
from coda.apps.publications.dto import parse_publication
from coda.apps.publications.models import Publication as PublicationModel
from coda.apps.publications.services import publication_create, publication_update
from coda.author import AuthorId
from coda.publication import PublicationId
from tests import factory
from tests.assertions import assert_publication_equal


@pytest.fixture
def author() -> Author:
    return factory.db_author()


@pytest.fixture
def journal() -> Journal:
    return factory.db_journal()


@pytest.mark.django_db
def test__create_publication__creates_a_publication_based_on_given_data(
    author: Author, journal: Journal
) -> None:
    publication_dto = factory.publication_dto(journal.pk)
    publication = parse_publication(publication_dto)
    new_id = publication_create(publication, AuthorId(author.pk))

    author_dto = author_dto_from_model(author)
    publication_in_db = PublicationModel.objects.get(pk=new_id)
    assert_publication_equal(publication_dto, author_dto, publication_in_db)


@pytest.mark.django_db
def test__create_publication__without_publication_date__sets_date_to_none(
    author: Author, journal: Journal
) -> None:
    publication_dto = factory.publication_dto(journal.pk)
    publication = parse_publication(publication_dto)
    new_id = publication_create(publication, AuthorId(author.pk))

    author_dto = author_dto_from_model(author)
    publication_in_db = PublicationModel.objects.get(pk=new_id)
    assert_publication_equal(publication_dto, author_dto, publication_in_db)


@pytest.mark.django_db
def test__update_publication__updates_publication_based_on_given_data() -> None:
    publication = factory.db_publication()
    new_journal = factory.db_journal()
    new_publication_data = factory.publication_dto(new_journal.pk)
    new_publication = parse_publication(new_publication_data, id=PublicationId(publication.pk))

    publication_update(new_publication)

    publication.refresh_from_db()
    author = author_dto_from_model(cast(Author, publication.submitting_author))
    assert_publication_equal(new_publication_data, author, publication)
