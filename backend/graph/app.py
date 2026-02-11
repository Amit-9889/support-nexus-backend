from langgraph.graph import StateGraph,START,END
from backend.agents.intent_detection_agent import Intent
from backend.Nodes.Validator import intent_validator
from backend.agents.SQL_query_agent import Sql_agent
from backend.Database_utility.Order_query_node import OrderQueryNode
from backend.Database_utility.postgres_db import PostgresDB
from backend.agents.answer_agent import AnswerAgent
from backend.state.agent_state import AgentState
from langchain_groq import ChatGroq
from backend.agents.policy_agent import PolicyAgent
from backend.agents.human_agent import HumanAgent

class AgentGraph:

    def __init__(self):
        pass
    ### DB Utility 
    def final_workflow(self):
        
        graph = StateGraph(AgentState)

        db = PostgresDB({
        "host": "localhost",
        "user": "genai_user",
        "password": "genai_pass",
        "database": "genai_db",
        "port": 5432,
        })

        ## LLM utility


        llm =  ChatGroq(model_name="llama-3.3-70b-versatile",temperature=0.3)
        ## Intent detection node
        intent = Intent(llm).intent_agent

        ## User Query validation
        validator = intent_validator().validate_order

        ## SQL Query generator
        sql_generator = Sql_agent(llm).create_sql_query

        ## Database connection and query executor
        sql_executor = OrderQueryNode(db)

        ## Answer node using llm to restructure answer and show to user
        answer = AnswerAgent(llm).answer

        ## Policy answer related Node
        policy = PolicyAgent(llm).policy_agent

        ## Human agent Node
        human = HumanAgent(agent_email="iamitkumar2007@gmail.com",  ## Human agent email
                           ticket_id="45291",
                           customer_email="iamitkumar2007@gmail.com", ## Customer email
                           issue_summary="Customer requested refund after delivery, claims item was damaged.").send_escalation_email

        ## Writing conditional method


        def route_after_validator(state:AgentState):
            if not state.get('order_id_required') and state.get('user_id') and state["intent"]=='ORDER':
                return 'ready'

            if (not state.get('user_id') or not state.get('order_id')) and state['order_id_required']:
                return 'need_info'

            return 'ready'

        ## Route identification for intent detection

        def route_after_intent(state:AgentState):
            if state['intent'] == 'ORDER':
                return 'order'
            
            elif state['intent'] == 'POLICY':
                return 'policy'
            
            else:
                return 'human'
        ## Now connecting Nodes to graph

        graph.add_node("intent",intent)
        graph.add_node("validator",validator)
        graph.add_node("sql_generator",sql_generator)
        graph.add_node("sql_executor",sql_executor)
        graph.add_node("answer",answer)
        graph.add_node("policy",policy)
        graph.add_node("human",human)
        ## Now Connecting Nodes with edges


        graph.add_edge(START,"intent")
        # graph.add_edge("intent","validator")
        graph.add_conditional_edges("intent",
                                   route_after_intent,{
                                       'order':"validator",
                                       'policy':"policy",
                                       'human':"human"
                                       
                                   })
        graph.add_conditional_edges("validator",
                                route_after_validator,{
                                    'need_info':END,
                                    'ready':"sql_generator"
                                }
                                )


        graph.add_edge("sql_generator","sql_executor")
        graph.add_edge("sql_executor","answer")
        graph.add_edge("answer",END)
        graph.add_edge("policy",END)
        graph.add_edge("human",END)
        workflow = graph.compile()

        return workflow
    #### 
