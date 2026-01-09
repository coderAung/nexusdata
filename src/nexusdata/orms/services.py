from abc import ABC

from nexusdata.asyncs.context import AsyncRepositoryContext
from nexusdata.legacy.contexts import RepositoryContext


class NexusService(RepositoryContext, ABC):pass

class AsyncNexusService(AsyncRepositoryContext, ABC):pass