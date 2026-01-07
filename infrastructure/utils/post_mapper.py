from core.entities import PostData


def extract_post_data(data: dict) -> PostData:
    post = data

    return PostData(
        post_id=post["id"],
        author_id=post["creator"]["id"],
        title=post["title"],
        published_at=post["firstPublishedAt"],
        subtitle=post["extendedPreviewContent"]["subtitle"],
        clap_count=post["clapCount"],
        responses_count=post["postResponses"]["count"],
        reading_time=post["readingTime"],
        collection_id=post["collection"]["id"] if post["collection"] else None
    )


if __name__ == "__main__":
    pass