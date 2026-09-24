import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError
from app.support.types import Repository, CheckResult, Money, money


def error(code, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == code


def invoke(service, method, *args, **kwargs):
    return api.call(service, method, *args, **kwargs)

def test_description():
    from app.domain.authorization import AuthorizationRequest
    from app.support.types import NamedCheck,CHECK_NAMES
    item=AuthorizationRequest("TX-1",[NamedCheck(n,CheckResult(True)) for n in CHECK_NAMES])
    assert item.describe()=="TX-1:6 checks"
