class UserRepository:
    def save(self, user):
        raise NotImplementedError

    def exists(self, user_id: str) -> bool:
        raise NotImplementedError