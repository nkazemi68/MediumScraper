from core.entities import UserData


def extract_user_data(data: dict) -> UserData:
    user = data["data"]["userResult"]

    return UserData(
        user_id=user["id"],
        username=user["username"],
        name=user["name"],
        bio=user["bio"],
        image_id=user["imageId"],
        subdomain=user["customDomainState"]["live"]["domain"] if user["hasSubdomain"] else None,
        is_book_author=user["verifications"]["isBookAuthor"],
        membership_data=user["membership"],
        follower_count=user["socialStats"]["followerCount"],
        following_count=user["socialStats"]["followingCount"],
        user_meta=user["userMeta"],
        about=user["about"],
    )
