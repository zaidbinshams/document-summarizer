import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [summaryLength, setSummaryLength] = useState("medium");
  const [result, setResult] = useState(null);

  const apiUrl = import.meta.env.VITE_API_URL;

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    const allowedTypes = [
      "application/pdf",
      "image/jpeg",
      "image/png",
      "image/webp",
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      setMessage("Please upload a PDF, JPG, PNG, or WEBP file.");
      return;
    }

    setFile(selectedFile);
    setMessage("");
    setResult(null);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      setMessage("Please select a document first.");
      return;
    }

    setLoading(true);
    setMessage("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const extractResponse = await fetch(
        `${apiUrl}/api/extract`,
        {
          method: "POST",
          body: formData,
        }
      );

      const extractedData = await extractResponse.json();

      if (!extractResponse.ok) {
        throw new Error(
          extractedData.detail || "Text extraction failed"
        );
      }

      const summarizeResponse = await fetch(
        `${apiUrl}/api/summarize`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: extractedData.text,
            length: summaryLength,
          }),
        }
      );

      const summaryData = await summarizeResponse.json();

      if (!summarizeResponse.ok) {
        throw new Error(
          summaryData.detail || "Summary generation failed"
        );
      }

      setResult(summaryData);
      setMessage(`Successfully processed ${file.name}`);
    } catch (error) {
      setMessage(error.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>Document Summary Assistant</h1>

          <p className="subtitle">
            Upload a PDF or image and generate an AI-powered summary.
          </p>
        </header>

        <main>
          <div className="card">
            <div
              className={`upload-box ${dragging ? "dragging" : ""}`}
              onDragOver={(e) => {
                e.preventDefault();
                setDragging(true);
              }}
              onDragLeave={() => setDragging(false)}
              onDrop={handleDrop}
            >
              <p>Drag & drop your document here</p>
              <span>or</span>

              <label className="browse-button">
                Browse Files

                <input
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png,.webp"
                  onChange={(e) => handleFile(e.target.files[0])}
                  hidden
                />
              </label>
            </div>

            {file && (
              <div className="file-info">
                <strong>Selected file:</strong> {file.name}
              </div>
            )}

            <div className="summary-options">
              <h3>Summary Length</h3>

              <div className="length-buttons">
                {["short", "medium", "long"].map((length) => (
                  <button
                    key={length}
                    className={
                      summaryLength === length ? "active" : ""
                    }
                    onClick={() => setSummaryLength(length)}
                    disabled={loading}
                  >
                    {length.charAt(0).toUpperCase() + length.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            <button
              className="summarize-button"
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? (
                <span className="loading">
                  <span className="spinner"></span>
                  Analyzing document...
                </span>
              ) : (
                "Generate Summary"
              )}
            </button>

            {message && <p className="message">{message}</p>}
          </div>

          {result && (
            <div className="results">
              <section className="result-card">
                <h2>Summary</h2>
                <p>{result.summary}</p>
              </section>

              <section className="result-card">
                <h2>Key Points</h2>

                <ul>
                  {result.key_points.map((point, index) => (
                    <li key={index}>{point}</li>
                  ))}
                </ul>
              </section>
            </div>
          )}
        </main>

        <footer className="footer">
          <span>Document Summary Assistant</span>

          <a
            href="https://github.com/zaidbinshams/document-summarizer"
            target="_blank"
            rel="noopener noreferrer"
          >
            View on GitHub
          </a>
        </footer>
      </div>
    </div>
  );
}

export default App;