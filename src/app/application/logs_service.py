from app.domain.ports import LogsRepoPort

class LogsService:
    def __init__(self, repo:LogsRepoPort):
        self.repo = repo

    def listar(self):
        return self.repo.listar()