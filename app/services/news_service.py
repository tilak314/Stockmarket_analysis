import feedparser

from urllib.parse import quote

from datetime import datetime, timezone, timedelta

from difflib import SequenceMatcher

import re


# Words that don't help identify a news event
STOP_WORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "from",
    "at",
    "by",
    "is",
    "are",
    "was",
    "were",
    "as",
    "after",
    "before",
    "today",
    "shares",
    "share",
    "stock",
    "stocks",
    "company",
    "limited",
    "ltd",
}


def normalize_title(title: str):

    title = title.lower()

    # Remove punctuation
    title = re.sub(r"[^a-z0-9\s]", " ", title)

    words = title.split()

    words = [
        word
        for word in words
        if word not in STOP_WORDS
    ]

    return set(words)


def calculate_similarity(title1: str, title2: str):

    words1 = normalize_title(title1)
    words2 = normalize_title(title2)

    if not words1 or not words2:
        return 0

    # Jaccard similarity
    intersection = words1.intersection(words2)
    union = words1.union(words2)

    jaccard = len(intersection) / len(union)

    # Sequence similarity
    sequence = SequenceMatcher(
        None,
        title1.lower(),
        title2.lower()
    ).ratio()

    # Combined score
    return (
        (jaccard * 0.7)
        +
        (sequence * 0.3)
    )


def get_company_news(
    company_name: str,
    ticker: str,
    limit: int = 5,
    days: int = 7
):

    clean_ticker = ticker.replace(".NS", "").replace(".BO", "")

    query = quote(
        f'"{company_name}" OR "{clean_ticker}"'
    )

    url = (
        "https://news.google.com/rss/search"
        f"?q={query}"
        "&hl=en-IN"
        "&gl=IN"
        "&ceid=IN:en"
    )

    feed = feedparser.parse(url)

    now = datetime.now(timezone.utc)

    cutoff_time = now - timedelta(days=days)

    candidates = []

    # -----------------------------------------
    # Collect recent articles
    # -----------------------------------------

    for entry in feed.entries:

        published_struct = entry.get(
            "published_parsed"
        )

        if not published_struct:
            continue

        published_datetime = datetime(
            published_struct.tm_year,
            published_struct.tm_mon,
            published_struct.tm_mday,
            published_struct.tm_hour,
            published_struct.tm_min,
            published_struct.tm_sec,
            tzinfo=timezone.utc
        )

        # Ignore old articles
        if published_datetime < cutoff_time:
            continue

        title = entry.get(
            "title",
            ""
        ).strip()

        if not title:
            continue

        source_name = None

        if hasattr(entry, "source"):

            source_name = entry.source.get(
                "title"
            )

        candidates.append({
            "title": title,

            "link": entry.get(
                "link"
            ),

            "source": source_name,

            "published": published_datetime.isoformat(),

            "published_datetime":
                published_datetime
        })

    # -----------------------------------------
    # Sort newest first
    # -----------------------------------------

    candidates.sort(
        key=lambda x: x["published_datetime"],
        reverse=True
    )

    # -----------------------------------------
    # Group similar news events
    # -----------------------------------------

    events = []

    for article in candidates:

        matched_event = None

        for event in events:

            similarity = calculate_similarity(
                article["title"],
                event["representative"]["title"]
            )

            if similarity >= 0.45:

                matched_event = event
                break

        if matched_event:

            matched_event["articles"].append(
                article
            )

        else:

            events.append({
                "representative": article,
                "articles": [article]
            })

    # -----------------------------------------
    # Pick the best article from each event
    # -----------------------------------------

    final_news = []

    for event in events:

        articles = event["articles"]

        # Newest article first
        articles.sort(
            key=lambda x: x["published_datetime"],
            reverse=True
        )

        best_article = articles[0]

        final_news.append({
            "title": best_article["title"],
            "link": best_article["link"],
            "source": best_article["source"],
            "published": best_article["published"],

            # Useful for understanding
            # how many publications reported
            # the same event
            "reports_count": len(articles)
        })

        if len(final_news) >= limit:
            break

    return final_news