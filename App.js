import React, { useState } from "react";

const App = () => {
    const [file, setFile] = useState(null);
    const [filename, setFilename] = useState("");
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");

    const uploadFile = async () => {
        if (!file) return alert("Select a PDF first!");

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("http://localhost:8000/upload_pdf/", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        setFilename(data.filename);
    };

    const askQuestion = async () => {
        if (!question) return alert("Enter a question!");

        const formData = new FormData();
        formData.append("question", question);
        formData.append("filename", filename);

        const response = await fetch("http://localhost:8000/ask_question/", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        setAnswer(data.answer);
    };

    return (
        <div style={{ padding: "20px" }}>
            <h2>PDF Q&A App</h2>
            
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            <button onClick={uploadFile}>Upload PDF</button>

            <br /><br />

            <input
                type="text"
                placeholder="Ask a question..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
            />
            <button onClick={askQuestion}>Get Answer</button>

            <h3>Answer: {answer}</h3>
        </div>
    );
};

export default App;
