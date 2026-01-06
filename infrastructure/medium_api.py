class MediumApi:
    _base_url = "https://medium.com/"
    _graphql_path = _base_url + "_/graphql"

    async def send_request_with_post_method(self, headers: dict, body: dict) -> dict:
        raise NotImplementedError


class Medium