from fastapi import FastAPI, UploadFile, File, Form # type: ignore
from fastapi.responses import JSONResponse # type: ignore
import fitz  # type: ignore # PyMuPDF for PDF text extraction
import os
from pathlib import Path
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader # type: ignore

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

documents = {}  # Stores extracted text in-memory for demo

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = Path(UPLOAD_DIR) / file.filename
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text from PDF
    pdf_document = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in pdf_document])

    documents[file.filename] = text  # Store extracted text
    return {"filename": file.filename, "message": "PDF uploaded successfully"}

@app.post("/ask_question/")
async def ask_question(question: str = Form(...), filename: str = Form(...)):
    if filename not in documents:
        return JSONResponse(content={"error": "PDF not found"}, status_code=400)

    text_content = documents[filename]
    
    # Simple implementation using LlamaIndex
    reader = SimpleDirectoryReader(input_files=[text_content])
    index = GPTVectorStoreIndex.from_documents(reader.load_data())
    
    response = index.query(question)

    return {"answer": response.response}

