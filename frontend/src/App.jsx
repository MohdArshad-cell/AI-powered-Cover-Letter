import { useState } from 'react';
import jsPDF from 'jspdf';
import './App.css';

function App() {
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [generatedCoverLetter, setGeneratedCoverLetter] = useState(''); // Renamed state
  const [isLoading, setIsLoading] = useState(false);
  const [copyButtonText, setCopyButtonText] = useState('Copy Text');

  const handleSubmit = async () => {
    setIsLoading(true);
    setCopyButtonText('Copy Text');
    setGeneratedCoverLetter('Generating your cover letter...'); // Updated text
    try {
      // *** CHANGE: Updated API endpoint ***
      const response = await fetch('http://localhost:8080/api/generate-cover-letter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume, jobDescription }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Network response was not ok: ${errorText}`);
      }

      const data = await response.json();
      // *** CHANGE: Updated response field ***
      setGeneratedCoverLetter(data.generatedCoverLetter);
    } catch (error) {
      console.error('Error:', error);
      setGeneratedCoverLetter(`Failed to generate cover letter. Please check the console for errors. Details: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePdfDownload = () => {
    const doc = new jsPDF();
    const text = generatedCoverLetter;

    // The splitTextToSize method automatically handles text wrapping
    const lines = doc.splitTextToSize(text, 180); // 180 is the max width of the text line

    doc.text(lines, 10, 10); // Add the text to the PDF
    doc.save('cover_letter.pdf'); // Save the PDF
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedCoverLetter).then(() => {
      setCopyButtonText('Copied!');
      setTimeout(() => {
        setCopyButtonText('Copy'); // Update reset text
      }, 2000); 
    }, (err) => {
      console.error('Could not copy text: ', err);
      setCopyButtonText('Failed!');
    });
  };

  return (
    <>
      <div className="background-aurora"></div>
      <div className="app-container">
        
        <div className="nav-panel">
          <div>
            <h1 style={{ textAlign: 'left', fontSize: '1.8rem', color: 'var(--accent-cyan)', marginBottom: '2rem' }}>
              AI Cover Letter Generator
            </h1>
          </div>
          <button
            className="btn btn-primary make-button"
            onClick={handleSubmit}
            disabled={isLoading || !resume || !jobDescription}
          >
            {isLoading ? 'Generating...' : 'Generate My Cover Letter'}
          </button>
        </div>

        <div className="editor-panel">
          <div className="form-section">
            <div className="form-group">
              <h2>Your Resume</h2>
              <textarea
                value={resume}
                onChange={(e) => setResume(e.target.value)}
                placeholder="Paste your full resume here..."
              />
            </div>
            <div className="form-group">
              <h2>Job Description</h2>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
              />
            </div>
          </div>
        </div>

        <div className="preview-panel">
          <div className="preview-header">
            <h2>Generated Cover Letter</h2>
            <div className="download-buttons">
    <button onClick={handleCopy} disabled={!generatedCoverLetter || isLoading || generatedCoverLetter.startsWith('Failed')} className="btn btn-primary">
      {copyButtonText === 'Copied!' ? 'Copied!' : 'Copy'} {/* Changed Text */}
    </button>
    <button onClick={handlePdfDownload} disabled={!generatedCoverLetter || isLoading || generatedCoverLetter.startsWith('Failed')} className="btn btn-primary">
      Download {/* Changed Text */}
    </button>
</div>
          </div>
          <pre id="preview-content">
            {generatedCoverLetter}
          </pre>
          
        </div>

      </div>
    </>
  );
}

export default App;