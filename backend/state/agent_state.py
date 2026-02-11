from typing import TypedDict,List,Optional

class AgentState(TypedDict,total=False):

    question : str
    intent : str
    answer : str
    user_id : str
    order_id : str
    sql_query : str
    db_result : dict | None
    order_id_required : bool