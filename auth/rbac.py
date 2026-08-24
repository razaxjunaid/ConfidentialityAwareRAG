ROLE_CLEARANCE = {
    "viewer": 1,
    "staff": 2,
    "senior": 3,
    "executive": 4
}


CLASSIFICATION_LEVEL = {
    "public": 1,
    "internal": 2,
    "confidential": 3,
    "highly_confidential": 4
}


def get_clearance(role: str):
    return ROLE_CLEARANCE.get(role.lower(), 0)


def can_access(user_role: str, document_classification: str):
    user_clearance = get_clearance(user_role)

    document_level = CLASSIFICATION_LEVEL.get(
        document_classification.lower(),
        0
    )

    return user_clearance >= document_level