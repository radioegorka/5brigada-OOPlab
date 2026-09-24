from app.domain.authorization import AuthorizationResult


def make_entity(transaction_id, checks):
    return {"transaction_id": transaction_id, "checks": tuple(checks)}


def _new_legacy_service():return {}

def view(request):return dict(request)


def invoke(service, method, request):
    if method != "authorize":raise ValueError(method)
    failures = [check for check in request["checks"] if not check.result.allowed]
    return AuthorizationResult.deny((failures[0].result.code,)) if failures else AuthorizationResult.allow()



def new_service():return _new_legacy_service()