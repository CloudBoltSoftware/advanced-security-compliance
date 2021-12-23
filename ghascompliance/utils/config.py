import os
from typing import ClassVar
import yaml
from dataclasses import dataclass

from ghascompliance.utils.dataclasses import _dataclass_from_dict
from ghascompliance.reporting.models import *
from ghascompliance.utils.octouri import validateUri


@dataclass
class PolicyConfig:
    instance: str = "https://github.com"
    repository: str = None
    path: str = None
    branch: str = None

    severity: str = "Error"

    display: bool = False

    def __post_init__(self):
        if self.path:
            uri = validateUri(self.path)
            if uri.repository:
                self.repository = uri.repository
                self.branch = uri.branch
                self.path = uri.path


@dataclass
class ThreatModelConfig:
    source: str = None

    high: PolicyConfig = None
    normal: PolicyConfig = None
    low: PolicyConfig = None


@dataclass
class CheckersConfig:
    codescanning: bool = True
    dependabot: bool = True
    dependencies: bool = True
    licensing: bool = True
    secretscanning: bool = True


@dataclass
class GitHubConfig:
    instance: str = None
    repository: str = None


@dataclass
class Paths:
    policy_repository: ClassVar[str] = None


@dataclass
class Config:
    name: str = "Configuration"
    github: GitHubConfig = GitHubConfig()

    organization: bool = False

    policy: PolicyConfig = PolicyConfig()

    threat_models: ThreatModelConfig = None

    checkers: CheckersConfig = CheckersConfig()

    reporting: ReportingConfig = None

    @staticmethod
    def load(path: str):
        if not os.path.exists(path):
            return

        with open(path) as handle:
            data = yaml.safe_load(handle)

        return _dataclass_from_dict(Config, data)
