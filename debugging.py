# from llm.chatollama import ChatOllamaBot
# bot = ChatOllamaBot()
# # print(bot.chat("What are the prerequisites of the course CIIC 4151 (Design Project)?"))
# print("Now Starting")
# # print(bot.chat("How are grades divided in the INSO 5111 course?"))
# print(bot.chat("What are the textbooks used in the Machine Learning course?"))
# # print(bot.chat("Tell me at least 3 topics that are taught in the introduction to database (CIIC4060) course"))

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

question = "How are grades divided in the Database Systems course?"
emb = model.encode(question)
embedding_text = str(emb.tolist())

print(embedding_text)
