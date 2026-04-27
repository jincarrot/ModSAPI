# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

class Systems:

    _client = None

    @property
    def client(self):
        if self._client:
            return self._client
        client = clientApi.GetSystem("ModSAPI", "client")
        self._client = client
        return client

systems = Systems()