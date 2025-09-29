import { useState } from 'react';
import { saveAs } from 'file-saver';
import './App.css';

function App() {
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [tailoredResume, setTailoredResume] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // --- NEW: State to manage the copy button's text ---
  const [copyButtonText, setCopyButtonText] = useState('Copy Code');

  const handleSubmit = async () => {
    setIsLoading(true);
    setCopyButtonText('Copy Code'); // Reset copy button on new submission
    setTailoredResume('Generating your tailored resume...');
    try {
      const response = await fetch('http://localhost:8080/api/tailor-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume, jobDescription }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Network response was not ok: ${errorText}`);
      }

      const data = await response.json();
      setTailoredResume(data.tailoredResume);
    } catch (error) {
      console.error('Error:', error);
      setTailoredResume(`Failed to tailor resume. Please check the console for errors. Details: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTxtDownload = () => {
    const blob = new Blob([tailoredResume], { type: 'text/plain;charset=utf-8' });
    saveAs(blob, 'tailored_resume.txt');
  };

  // --- NEW: Function to handle copying to clipboard ---
  const handleCopy = () => {
    navigator.clipboard.writeText(tailoredResume).then(() => {
      setCopyButtonText('Copied!');
      setTimeout(() => {
        setCopyButtonText('Copy Code');
      }, 2000); // Reset after 2 seconds
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
              AI Resume Maker
            </h1>
          </div>
          <button
            className="btn btn-primary make-button"
            onClick={handleSubmit}
            disabled={isLoading || !resume || !jobDescription}
          >
            {isLoading ? 'Tailoring...' : 'Tailor My Resume'}
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
            <h2>Tailored Resume Preview</h2>
            <div className="download-buttons">
            {/* --- NEW: Copy Button Added Here --- */}
            <button onClick={handleCopy} disabled={!tailoredResume || isLoading || tailoredResume.startsWith('Failed')} className="btn btn-primary">
              {copyButtonText}
            </button>
            <button onClick={handleTxtDownload} disabled={!tailoredResume || isLoading || tailoredResume.startsWith('Failed')} className="btn btn-primary">
              Download TXT
            </button>
          </div>
          </div>
          <pre id="preview-content">
            {tailoredResume}
          </pre>
          
        </div>

      </div>
    </>
  );
}

export default App;