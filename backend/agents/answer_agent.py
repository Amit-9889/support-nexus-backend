from langchain_core.prompts import PromptTemplate
from backend.state.agent_state import AgentState
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
load_dotenv()


class AnswerAgent:

    def __init__(self, model):
        self.model = model

    def answer(self, state: AgentState):

        db_result = state.get("db_result")

        # Guard: nothing to answer from DB
        if not db_result:
            return {
                "answer": "I couldn’t find any order information to answer your query."
            }

        prompt = PromptTemplate(
                                template="""
                                You are a great explainer.
                                Analyze the user question and the database result, then generate
                                a clear, meaningful, and concrete summary.
                                If you not find any relevant result from databse, please tell , I am sorry.

                                Strict instruction:
                                - Don't overexplain the answer.
                                - Keep answer short and clear.
                                - Don't assume anything by yourself except factual information.
                                
                                Answer example:
                                - Before generating answer do proper formatting , like remove "\" from answer and any stop symbols which makes readability complex.
                                - The status of your order PC12345 is \"completed\".

                                Question:
                                {question}

                                Database Result:
                                {db_result}
                                """,
                                    input_variables=["question", "db_result"]
                                )

        final_prompt = prompt.format(
            question=state.get("question"),
            db_result=db_result
        )

        parser = StrOutputParser()


        # answer = self.model.invoke(final_prompt).content
        chain = self.model | parser

        answer = chain.invoke(final_prompt)

        return {"answer": answer}

