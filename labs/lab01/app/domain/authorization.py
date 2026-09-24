from dataclasses import dataclass
from app.support.types import identifier, NamedCheck, CHECK_NAMES
from app.support.errors import DomainError
# ЛР1: класс AuthorizationRequest вместо словаря.
@dataclass(frozen=True)
class AuthorizationResult:
    approved: bool
    reason: str | None
    failed_codes: tuple
    def __post_init__(self):
        codes = tuple(self.failed_codes)
        if type(self.approved) is not bool:
            raise DomainError("INVALID_RESULT")
        if self.approved:
            if self.reason is not None or codes:
                raise DomainError("INVALID_RESULT")
        elif (not codes or not isinstance(self.reason, str) or not self.reason.strip()
              or codes[0] != self.reason or any(not isinstance(code,str) or not code.strip() for code in codes)):
            raise DomainError("INVALID_RESULT")
        object.__setattr__(self, "failed_codes", codes)
    @classmethod
    def allow(cls):
        return cls(True, None, ())
    @classmethod
    def deny(cls, codes):
        codes = tuple(codes)
        if not codes:
            raise DomainError("INVALID_RESULT")
        return cls(False, codes[0], codes)