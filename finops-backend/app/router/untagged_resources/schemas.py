from dataclasses import dataclass


@dataclass
class ResourceTagConfig:
    resource_type: str
    service: str
    region: str
    resource_name_or_id: str
    resource_arn: str


@dataclass
class Tag:
    key: str
    value: str


@dataclass
class TagInput:
    resources: list[ResourceTagConfig]
    tags: list[Tag]