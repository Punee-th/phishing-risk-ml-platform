"""URL canonicalisation utilities."""

from urllib.parse import urlsplit, urlunsplit


def canonicalize_url(url: str) -> str:
    """
    Convert a URL into the canonical format used during model training.

    Rules:
    - Remove surrounding whitespace.
    - Add HTTPS when the scheme is missing.
    - Lowercase the scheme and hostname.
    - Remove default HTTP/HTTPS ports.
    - Treat an empty path and root slash as equivalent.
    - Remove URL fragments.
    - Preserve meaningful paths and query parameters.

    Args:
        url: Raw URL supplied by the user.

    Returns:
        Canonicalised URL string.
    """
    url = str(url).strip()

    if "://" not in url:
        url = "https://" + url

    parsed = urlsplit(url)

    scheme = parsed.scheme.lower()
    hostname = (parsed.hostname or "").lower()

    userinfo = ""

    if parsed.username is not None:
        userinfo = parsed.username

        if parsed.password is not None:
            userinfo += ":" + parsed.password

        userinfo += "@"

    try:
        port = parsed.port
    except ValueError:
        port = None

    default_port = (
        (scheme == "https" and port == 443)
        or (scheme == "http" and port == 80)
    )

    port_text = (
        f":{port}"
        if port is not None and not default_port
        else ""
    )

    netloc = userinfo + hostname + port_text

    path = "" if parsed.path in ("", "/") else parsed.path

    return urlunsplit(
        (
            scheme,
            netloc,
            path,
            parsed.query,
            ""
        )
    )
