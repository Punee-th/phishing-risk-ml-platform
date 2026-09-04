"""Lexical URL feature extraction for the phishing model."""

import ipaddress
import re
from urllib.parse import urlsplit

from src.canonicalizer import canonicalize_url


FEATURE_NAMES = [
    "url_length",
    "domain_length",
    "is_domain_ip",
    "tld_length",
    "subdomain_count",
    "letter_count",
    "letter_ratio",
    "digit_count",
    "digit_ratio",
    "equals_count",
    "question_mark_count",
    "ampersand_count",
    "is_https",
]


def extract_engineered_features(url: str) -> dict:
    """Extract the 13 features used by model version 1.1.0."""

    cleaned_url = canonicalize_url(url)
    parsed = urlsplit(cleaned_url)
    domain = (parsed.hostname or "").lower()

    url_length = len(cleaned_url)
    domain_length = len(domain)

    try:
        ipaddress.ip_address(domain)
        is_domain_ip = 1
    except ValueError:
        is_domain_ip = 0

    domain_parts = [
        part for part in domain.split(".")
        if part
    ]

    tld_length = (
        len(domain_parts[-1])
        if domain_parts
        else 0
    )

    subdomain_count = max(
        len(domain_parts) - 2,
        0
    )

    letter_count = len(
        re.findall(r"[A-Za-z]", cleaned_url)
    )

    digit_count = len(
        re.findall(r"[0-9]", cleaned_url)
    )

    letter_ratio = (
        letter_count / url_length
        if url_length > 0
        else 0
    )

    digit_ratio = (
        digit_count / url_length
        if url_length > 0
        else 0
    )

    return {
        "url_length": url_length,
        "domain_length": domain_length,
        "is_domain_ip": is_domain_ip,
        "tld_length": tld_length,
        "subdomain_count": subdomain_count,
        "letter_count": letter_count,
        "letter_ratio": letter_ratio,
        "digit_count": digit_count,
        "digit_ratio": digit_ratio,
        "equals_count": cleaned_url.count("="),
        "question_mark_count": cleaned_url.count("?"),
        "ampersand_count": cleaned_url.count("&"),
        "is_https": int(parsed.scheme == "https"),
    }