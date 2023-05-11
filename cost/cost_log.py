from db.database import data_base
from db.model import CostLog


class CostLogManager:
    @staticmethod
    def insert(user, prompt_cost, complete_cost, model_version):
        cost_log = CostLog(username=user, prompt_cost=prompt_cost, complete_cost=complete_cost, model_version=model_version)
        data_base.insert(cost_log)




