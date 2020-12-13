from injector import singleton, provider, Module

from tools.asyncio_postgres_client import AsyncPostgresClient

from configs.config_service import ConfigService


class CoreModule(Module):
    @singleton
    @provider
    def provide_postgres_client(
        self, config_service: ConfigService
    ) -> AsyncPostgresClient:
        postgres_client = AsyncPostgresClient(config_service.pg_address)
        # TODO: check asyncio support
        ## TODO: await postgres_client.connect()

        return postgres_client
