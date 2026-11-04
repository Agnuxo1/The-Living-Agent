# Project: The Living Agent
# Copyright (c) 2026 Francisco Angulo de Lafuente
# ORCID: https://orcid.org/0009-0001-1634-7063
# Attribution record: 2026-11-04
# SPDX-License-Identifier: Apache-2.0

"""The Living Agent - Autonomous Chess-Grid research engine."""

__version__ = "1.0.0"
__author__ = "Francisco Angulo de Lafuente"
__license__ = "Apache-2.0"

from living_agent.grid import generate_grid, DIRECTIONS
from living_agent.llm_client import KoboldClient
from living_agent.agent import LivingAgent

__all__ = [
    "__version__",
    "generate_grid",
    "DIRECTIONS",
    "KoboldClient",
    "LivingAgent",
]
