from app.domain.ports import LogsRepoPort

class LogService:
    def __init__(self, repoPort:LogsRepoPort):
        self.repoLog = repoPort

    def list(self):
        return self.repoLog.list()