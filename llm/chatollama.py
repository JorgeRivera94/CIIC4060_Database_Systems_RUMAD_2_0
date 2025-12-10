from dao.syllabuses import SyllabusDAO
from dao.classes import ClassDAO
from sentence_transformers import SentenceTransformer
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List, Dict, Any, Optional
import re

_model = SentenceTransformer("all-mpnet-base-v2")

class ChatOllamaBot:
    def __init__(self, model: Optional[SentenceTransformer] = None):
        self.model = model or _model
        self.syllabus_dao = SyllabusDAO()
        self.class_dao = ClassDAO()

        # Get all cdesc
        raw_cdescs = self.class_dao.get_all_cdesc()
        # Flatten and dedupe
        self.cdesc_list: List[str] = sorted({row[0] for row in raw_cdescs if row and row[0]})
        self.cdesc_lower_map = {c.lower(): c for c in self.cdesc_list}

        self.prompt = PromptTemplate(
            template="""
                You are an assistant that answers questions about university courses using official syllabi.
                You are given text fragments extracted from PDFs. The text may contain noise such as '[UNK]' or missing
                punctuation; ignore that noise and focus on the meaning.
                When the question is about how grades are divided, evaluation strategies, or grading system, you must
                look for sections that mention things like 'evaluation strategies', 'quantity', 'percent', 'exams',
                'final exam', 'projects', or a table of percentages, and use those numbers to describe how grades are
                divided (e.g., '3 exams worth 45%, final exam 20%, project 35%'). \n
                Use the following documents and the conversation history to answer the question.
                If you don't know the answer, just say that you don't know.
                Use ten sentences maximum and keep the answer concise. \n
                Conversation history: \n{history} \n
                Documents: \n{documents} \n
                Question: {question} \n
                Answer:
                """,
            input_variables=["question", "documents", "history"],
        )

        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0,
        )

        self.rag_chain = self.prompt | self.llm | StrOutputParser()

    # Check if cname and ccode are in the question
    def _extract_course_from_question(self, question: str) -> tuple[Optional[str], Optional[str]]:
        m = re.search(r"\b([A-Za-z]{4})\s*-?\s*(\d{4})\b", question)
        if not m:
            return None, None
        cname = m.group(1).upper()
        ccode = m.group(2)
        return cname, ccode

    # Check if cdesc in question
    def _extract_cdesc_from_question(self, question: str) -> Optional[str]:
        q_lower = question.lower()

        # If "course" or "class" in question
        course_words = {"course", "class"}
        if not any(word in q_lower for word in course_words):
            return None

        # Short cdesc could be part of the conversation and maybe not reference a class like "data structures"
        matches: List[tuple[str, int]] = []
        for cdesc in self.cdesc_list:
            cdesc_lower = cdesc.lower()
            if cdesc_lower in q_lower:
                matches.append((cdesc, len(cdesc)))

        if not matches:
            return None

        # Return longest cdesc
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[0][0]

    def _clean_chunk(self, text: str) -> str:
        # Remove [UNK] tokens and normalize spaces
        text = text.replace("[UNK]", " ")
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _retrieve_context(self, emb, question: str) -> List[str]:
        embedding_text = str(emb.tolist())
        cname, ccode = self._extract_course_from_question(question)

        if cname and ccode:
            fragments = self.syllabus_dao.get_fragments_by_cname_ccode(embedding_text, cname, ccode)
        else:
            cdesc = self._extract_cdesc_from_question(question)
            if cdesc:
                fragments = self.syllabus_dao.get_fragments_by_cdesc(embedding_text, cdesc)
            else:
                fragments = self.syllabus_dao.get_fragments(embedding_text)

        context: List[str] = []
        for f in fragments:
            if len(f) > 3 and f[3] is not None:
                context.append(self._clean_chunk(str(f[3])))
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

        context = self._retrieve_context(emb, question)
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