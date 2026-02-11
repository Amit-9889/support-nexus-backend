from langchain_groq import ChatGroq
from dotenv import load_dotenv
from backend.Nodes.retriever import Retriever
from backend.state.agent_state import AgentState
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

class PolicyAgent:

    def __init__(self,llm):
        self.model = llm

    def policy_agent(self,state:AgentState):

        retriver = Retriever().retrive_context()
        query_context = retriver.invoke(state['question'])[0].page_content
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an expert policy analyst.
                You must answer strictly based on the provided context.
                If the answer is not explicitly present in the context, respond exactly with:
                "Sorry, I don't have the answer."

                Response rules:
                - Maximum 2 lines
                - Short, crisp, and precise
                - No assumptions, no external knowledge
                - No explanations or reasoning"""
                    ),
                    (
                        "human",
                        """Context:
                {context}

                Question:
                {question}"""
                    )
                ])


        final_prompt = prompt.format(question=state['question'],context=query_context)
        

        output = self.model.invoke(final_prompt).content

        return {"answer":output}
        