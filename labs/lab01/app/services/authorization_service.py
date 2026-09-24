from app.domain.authorization import AuthorizationRequest, AuthorizationResult


class AuthorizationService:
    def authorize(self, request):
        failures = request.failed_checks()

        if failures:
            return AuthorizationResult.deny((failures[0].result.code,))

        return AuthorizationResult.allow()


def make_entity(transaction_id, checks):
    return AuthorizationRequest(transaction_id, checks)


def view(request):
    return {
        "transaction_id": request.transaction_id,
        "checks": request.checks
    }


def invoke(service, method, request):
    if method != "authorize":
        raise ValueError(method)

    return service.authorize(request)


def new_service():
    return AuthorizationService()