# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ..config import Namespace

class Systems:

    _client = None

    @property
    def client(self):
        if self._client:
            return self._client
        client = clientApi.GetSystem(Namespace, "client")
        self._client = client
        return client

systems = Systems()