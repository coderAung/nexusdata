from abc import ABC

from nexusdata.asyncs.repositories import AsyncSessionRepository
from nexusdata.core.metadata.typings import MODEL, ID
from nexusdata.legacy.repositories import SimpleSessionRepository


class NexusRepository(SimpleSessionRepository[MODEL, ID], ABC):pass

class AsyncNexusRepository(AsyncSessionRepository[MODEL, ID], ABC):pass