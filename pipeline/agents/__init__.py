"""Агенты пайплайна: один этап = один агент = один артефакт."""

from pipeline.agents.architecture_api import ArchitectureApiAgent
from pipeline.agents.requirements import RequirementsAgent
from pipeline.agents.system_analysis import SystemAnalysisAgent
from pipeline.agents.ui import UiDesignAgent

__all__ = [
    "ArchitectureApiAgent",
    "RequirementsAgent",
    "SystemAnalysisAgent",
    "UiDesignAgent",
]