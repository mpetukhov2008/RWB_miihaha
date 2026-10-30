"""Агенты пайплайна: один этап = один агент = один артефакт."""

from pipeline.agents.architecture_api import ArchitectureApiAgent
from pipeline.agents.codegen_backend import CodegenBackendAgent
from pipeline.agents.codegen_frontend import CodegenFrontendAgent
from pipeline.agents.docs_agent import DocsAgent
from pipeline.agents.requirements import RequirementsAgent
from pipeline.agents.security_agent import SecurityReportAgent
from pipeline.agents.system_analysis import SystemAnalysisAgent
from pipeline.agents.tests_agent import TestsAgent
from pipeline.agents.ui import UiDesignAgent

__all__ = [
    "ArchitectureApiAgent",
    "CodegenBackendAgent",
    "CodegenFrontendAgent",
    "DocsAgent",
    "RequirementsAgent",
    "SecurityReportAgent",
    "SystemAnalysisAgent",
    "TestsAgent",
    "UiDesignAgent",
]