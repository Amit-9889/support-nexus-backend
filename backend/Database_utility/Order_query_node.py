from backend.Database_utility.postgres_db import PostgresDB
from backend.state.agent_state import AgentState

class OrderQueryNode:

    def __init__(self, db: PostgresDB):
        self.db = db

    def __call__(self, state: AgentState):

        sql = state.get("sql_query")

        # ARD GUARD — do nothing if no SQL
        if not sql:
            return {}

        result = self.db.fetch_one(sql)

        return {"db_result": result}
