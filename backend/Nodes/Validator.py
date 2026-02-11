from backend.state.agent_state import AgentState
import re
from typing import TypedDict


class intent_validator:

    def __init__(self):
        pass

    @classmethod
    def has_order_id(cls,text)->str | None:
        match = re.search(r'(?:#)?(PC\d{5,})', text)
        return match.group(1) if match else None

    def validate_order(self,state:AgentState):

        
        ## Checking if intent contains any if these : 1) Explicit ownership , 2) order identifier 3) Action on order
        if state['intent'] != 'ORDER':
            return{}
            
        order_id = intent_validator.has_order_id(state['question'])

        if state['intent'] == 'ORDER' and state['order_id_required']:
            print("order_type",type(order_id))
            print("Order id",order_id)
            if not order_id:
                    return {}
                
            if 'user_id' not in state:
                return{
                    "order_id":order_id
                }
            
            return {   
                    'user_id': state['user_id'], 
                    'order_id':order_id
                    }
        
        if state['intent'] == 'ORDER' and not state['order_id_required']:
             
            if 'user_id' not in state:
                return {}
            
            else:
                return{
                    'user_id': state['user_id']
                }

            
             

