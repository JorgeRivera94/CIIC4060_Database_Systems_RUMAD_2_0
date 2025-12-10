from charset_normalizer.md import is_separator
from pypdf import PdfReader
from os import listdir
from langchain_text_splitters import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from dao.docs import DocDAO
from dao.syllabuses import SyllabusDAO
from dao.classes import ClassDAO
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

files = listdir("./ETL/Extract/syllabuses")
print(files)

# Extract chunks
docDAO = DocDAO()
fraDAO = SyllabusDAO()
classDAO = ClassDAO()

for f in files:
    fname = "./ETL/Extract/syllabuses/" + f
    reader = PdfReader(fname)
    pdf_texts = [p.extract_text() for p in reader.pages]

    # Filter the empty strings
    pdf_texts = [text for text in pdf_texts if text]

    print("Frist page pf Document*************************")
    print(pdf_texts[0])
    print("END Document *****************************\n\n")

    # Split
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n", ". ", " ", ""],
        chunk_size=300,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False
    )
    character_split_texts = character_splitter.split_text(''.join(pdf_texts))

    print("See SPLIT 10 *************")
    print(character_split_texts[10])
    print()
    print("END SPLIT 10 *************\n\n")
    print(f"\nTotal chunks: {len(character_split_texts)}")

    print("DEBUG - see All Splits*************")
    [print(t) for t in character_split_texts]
    print()
    print("DEBUG End All Splits*************")

    # Token
    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=60, tokens_per_chunk=384)

    token_split_texts = []
    for text in character_split_texts:
        token_split_texts += token_splitter.split_text(text)

    print("All Token Split *************")
    i = 0
    for t in token_split_texts:
        print(i, " ", t)
        i += 1
    print("End AllToken Split *************\n\n")
    print(f"\nTotal Splitted chunks: {len(token_split_texts)}\n\n")

    # Insert document into table
    did = docDAO.insert_doc(f)

    i = 0
    for t in token_split_texts:
        emb = model.encode(t)
        print(i, " ", t)
        i += 1
        fraDAO.insert_syllabus(courseid=classDAO.get_class_by_name_and_code(f[0:4], f[5:9]), did=did, chunk=t, embedding_text=emb.tolist())

    print("Done file: " + f)