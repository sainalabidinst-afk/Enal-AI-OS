from enum import StrEnum


class PackStatus(StrEnum):
    DRAFT = "draft"
    TESTING = "testing"
    APPROVED = "approved"
    REJECTED = "rejected"
    REGISTERED = "registered"
    DEPRECATED = "deprecated"