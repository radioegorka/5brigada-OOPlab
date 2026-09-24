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

from app.support.types import NamedCheck,CHECK_NAMES

def checks_values(failures=None):
    failures=failures or {}
    return [NamedCheck(name,CheckResult(name not in failures,failures.get(name))) for name in CHECK_NAMES]

def request(failures=None):return api.make("TX-1",checks_values(failures))

def test_allow_and_decline():
    service=api.create()
    yes=invoke(service,"authorize",request())
    assert (yes.approved,yes.reason,yes.failed_codes)==(True,None,())
    no=invoke(service,"authorize",request({"FUNDS":"INSUFFICIENT_FUNDS"}))
    assert (no.approved,no.reason,no.failed_codes)==(False,"INSUFFICIENT_FUNDS",("INSUFFICIENT_FUNDS",))

def test_requests_are_independent_and_not_mutated():
    service=api.create()
    invoke(service,"authorize",request({"FUNDS":"INSUFFICIENT_FUNDS"}))
    safe=request()
    before=api.view(safe)
    assert invoke(service,"authorize",safe).approved
    assert api.view(safe)==before
