from dotenv import load_dotenv
from langchain_core.messages import SystemMessage,HumanMessage
from backend.state.agent_state import AgentState
import json
load_dotenv()

class Intent:

    def __init__(self,model):
        self.model = model


    def intent_agent(self,state:AgentState):

        messages = [
    SystemMessage(
        content="""
You are a strict Intent Classification Engine.

CRITICAL RULES (Follow strictly):

- Classify as ORDER only if the user message clearly refers to the user's own order(s),
  including order status, delivery, shipment, payment, or order history.
- Order ID is NOT mandatory for ORDER intent if the query refers to
  aggregated or personal order information (e.g., "my orders", "pending orders").
- If a message implies an order-related issue (e.g., delay, failure) but does not
  clearly establish ownership, classify as ORDER with confidence below 0.85.
- If there is ANY doubt or ambiguity, choose HUMAN.

--------------------------------
FILTERED HIGH-COVERAGE EXAMPLES
--------------------------------

HUMAN:
"Hi, I just want to understand what kind of help you provide."
"I’m not looking for anything specific, just need some guidance."
"Can you explain how things usually work here?"

ORDER:
"What is the status of my order 556677?"
"How many of my orders are pending or failed?"
"Can you give me a summary of my recent orders?"
"One of my orders seems delayed, can you check?"

POLICY:
"What is your refund policy if an order fails?"
"What does your policy say about delayed deliveries?"
"Can you explain the cancellation or return policy?"

--------------------------------
INTENT DEFINITIONS
--------------------------------

- ORDER:
  Mentions a specific order, multiple personal orders, transaction, payment,
  shipment, delivery status, or personal ownership (e.g., "my order",
  "my orders", order ID, tracking, payment made).

- POLICY:
  Asks about rules, terms, eligibility, refunds, cancellations, returns,
  or compensation WITHOUT referring to a specific personal order.

- HUMAN:
  General questions, greetings, exploration, vague requests,
  or unclear intent.

--------------------------------
ORDER ID REQUIREMENT LOGIC
--------------------------------

- Analyze the message and decide whether an order_id_required is False | True.
- If the query can be answered using user context or aggregated data,
  set "order_id_required": false.
- If a specific order must be identified or order id given in query then, set "order_id_required": true.

--------------------------------
OUTPUT FORMAT (JSON ONLY)
--------------------------------

{
  "intent": "ORDER" | "POLICY" | "HUMAN",
  "confidence": number between 0.0 and 1.0,
  "order_id_required": true | false
}

--------------------------------
CONFIDENCE GUIDELINES
--------------------------------

- 0.90 – 1.00 → Explicit ownership or order ID present
- 0.70 – 0.85 → Clear personal order context, no ID
- < 0.60     → Ambiguous, vague, or hypothetical

--------------------------------
STRICT RULES
--------------------------------

- Do NOT answer the user.
- Do NOT explain reasoning.
- Output JSON ONLY.
"""
    ),
    HumanMessage(content=state["question"])
]


        ## Invoking model with above question

        model_output = self.model.invoke(messages).content

      
        try:
            result = json.loads(model_output)

        except json.JSONDecodeError:
            result = {"intent":"HUMAN","confidence":0.0}

        intent = result.get("intent","HUMAN")
        order_id_required = result.get("order_id_required","False")
        

        #state["intent"] = intent
        return {
            "intent":intent,
            "order_id_required":order_id_required
        }

