from dao.syllabuses import SyllabusDAO
from sentence_transformers import SentenceTransformer
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List, Dict, Any, Optional

_model = SentenceTransformer("all-mpnet-base-v2")

class ChatOllamaBot:
    def __init__(self, encoder: Optional[SentenceTransformer] = None):
        self.model = encoder or _model

        self.prompt = PromptTemplate(
            template="""You are an assistant for question-answering tasks.
                Use the following documents and the conversation history to answer the question.
                If you don't know the answer, just say that you don't know.
                Use ten sentences maximum and keep the answer concise. \n
                Conversation history: {history} \n
                Documents: {documents} \n
                Question: {question} \n
                Answer:""",
            input_variables=["question", "documents", "history"],
        )

        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0,
        )

        self.rag_chain = self.prompt | self.llm | StrOutputParser()

    def _retrieve_context(self, emb) -> List[str]:
        dao = SyllabusDAO()
        fragments = dao.get_fragments(str(emb.tolist()))
        context: List[str] = []
        for f in fragments:
            if len(f) > 2 and f[3] is not None:
                context.append(f[3])
        return context

    def _format_history(
            self,
            history: List[Dict[str, Any]],
            max_messages: int = 10,
    ) -> str:
        if not history:
            return "No previous conversation."

        trimmed = history[-max_messages:]

        lines: List[str] = []
        for msg in trimmed:
            role = (msg.get("role") or "").lower()
            content = (msg.get("content") or "")
            if not content:
                continue

            if role == "user":
                prefix = "User"
            elif role == "assistant":
                prefix = "Assistant"
            else:
                prefix = "Other"

            lines.append(f"{prefix}: {content}")

        return "\n".join(lines) if lines else "No previous conversation."

    def chat(
            self,
            question: str,
            history: Optional[List[Dict[str, Any]]] = None,
    ) -> str:

        history = history or []

        # Embed question for retreival
        emb = self.model.encode(question)

        context = self._retrieve_context(emb)
        documents = "\n".join(context) if context else "No relevant documents found."
        history_str = self._format_history(history)

        answer = self.rag_chain.invoke(
            {
                "question": question,
                "documents": documents,
                "history": history_str,
            }
        )

        return answer