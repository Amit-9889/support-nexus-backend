from backend.state.agent_state import AgentState
from langchain_core.prompts import PromptTemplate
import re
from dotenv import load_dotenv

load_dotenv()

class Sql_agent:

    def __init__(self, model):
        self.model = model

    def clean_sql(self,sql: str) -> str:
        if not sql:
            return sql

        # Remove ```sql and ``` blocks
        sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
        sql = re.sub(r"```", "", sql)

        return sql.strip()

    def create_sql_query(self, state: AgentState):

        # 🚫 Do nothing if intent is not ORDER
        if state.get("intent") != "ORDER":
            return {}

        user_id = state.get("user_id")
        order_id = state.get("order_id")

        # 🚫 SQL agent assumes validation already happened
        if not user_id:
            return {}

        prompt_template = PromptTemplate(
            input_variables=["question", "user_id", "order_id"],
            template="""
You are a SQL query generator for a production backend system.

CRITICAL SECURITY RULES:
- Generate ONLY a single READ-ONLY SELECT statement.
- NEVER use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE.
- NEVER use SELECT *.
- NEVER infer missing values.
- NEVER access tables other than `orders` and `users`.
- ALWAYS filter by user_id.
- If order_id is provided, filter by order_id.
- If order_id is NOT provided, generate an aggregated or list query scoped to user_id.
- Return order_id in the SELECT clause.

Database schema:

orders(
    user_id VARCHAR,
    status VARCHAR,
    order_date TIMESTAMP,
    order_id VARCHAR
)
users(
    user_id VARCHAR,
    name VARCHAR,
    email_id VARCHAR,
    )

User query (context only):
"{question}"

Resolved inputs (authoritative):
- user_id: {user_id}
- order_id: {order_id}

Task:
Generate a safe SQL SELECT query.

Output:
SQL ONLY. No explanation.
"""
        )

        final_prompt = prompt_template.format(
            question=state["question"],
            user_id=user_id,
            order_id=order_id
        )

        raw_sql = self.model.invoke(final_prompt).content
        sql = self.clean_sql(raw_sql)

        return {"sql_query": sql}
