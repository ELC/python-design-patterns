import uuid

HIRING_NAMESPACE = uuid.UUID(int=5)


def deterministic_uuid(key: str) -> uuid.UUID:
    return uuid.uuid5(HIRING_NAMESPACE, key)


def employee_id(candidate_name: str) -> str:
    return f"EMP-{deterministic_uuid(candidate_name)}"
