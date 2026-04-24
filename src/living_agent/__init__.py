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
