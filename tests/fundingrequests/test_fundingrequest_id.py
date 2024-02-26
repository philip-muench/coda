import datetime

import pytest

from coda.apps.fundingrequests.models import FundingRequest
from tests.fundingrequests import factory


@pytest.mark.django_db
def test__fundingrequest__has_valid_id_pattern() -> None:
    request = FundingRequest.objects.create(
        publication=factory.publication(), estimated_cost=100, estimated_cost_currency="USD"
    )

    split_id = request.request_id.split("-")
    uuid_component = len(split_id[1])
    date_component = datetime.date(*map(int, split_id[2:]))
    assert split_id[0] == "coda"
    assert uuid_component == 6
    assert date_component == request.created_at.date()