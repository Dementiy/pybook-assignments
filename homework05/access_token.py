import argparse
import webbrowser


def get_access_token(client_id: int, scope: str) -> None:
    assert isinstance(client_id, int), "clinet_id must be positive integer"
    assert isinstance(scope, str), "scope must be string"
    assert client_id > 0, "clinet_id must be positive integer"
    url = f"""\
    https://oauth.vk.com/authorize?client_id={client_id}&\
    redirect_uri=https://oauth.vk.com/blank.hmtl&\
    scope={scope}&\
    &response_type=token&\
    display=page&\
    v=5.102\
    """.replace(
        " ", ""
    )
    webbrowser.open_new_tab(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="Application Id", type=int)
    parser.add_argument(
        "-s", dest="scope", help="Permissions bit mask", type=str, default="", required=False
    )
    args = parser.parse_args()
    get_access_token(args.client_id, args.scope)
