from backend.vector_database.vector_store import vector_db


class Retriever:

    def retrive_context(self):
            
        vector_query_method = vector_db().query()

        retriver = vector_query_method.as_retriever(
            search_type = "similarity_score_threshold",
            search_kwargs = {"k":3, "score_threshold":0.5}
        )

        # print(retriver.invoke("Maulana Azad National Institute of Technology")[0].page_content)

        return retriver