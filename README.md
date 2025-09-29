AI-Powered Resume Tailor
A full-stack web application that uses Google's Gemini AI to automatically tailor a resume to a specific job description, generating a professional LaTeX output.

## Tech Stack

Frontend: React.js, CSS3

Backend: Java, Spring Boot

AI / Scripting: Python, Google Gemini Pro

Formatting: LaTeX

Features
AI-Powered Tailoring: Ingests a resume and job description to generate a tailored version.

Advanced Prompting: Uses a sophisticated 4-step prompt chain for high-quality, strategic results.

Professional Output: Creates clean, compilable LaTeX code based on a professional template.

Download Options: Users can copy the code or download .txt and .pdf versions of the resume.

Architecture
The application uses a three-tier architecture:

Frontend (React): A user-friendly interface for input and to display the results.

Backend (Spring Boot): A Java-based REST API that orchestrates the process by calling the Python script.

Python Script: Manages the multi-step prompting logic with the Gemini API to produce the final LaTeX code.

Getting Started
Prerequisites
Java 17+

Maven

Node.js & npm

Python 3.8+

A LaTeX distribution (e.g., MiKTeX for Windows)

A Google Gemini API Key

Installation & Setup
Backend (Spring Boot)

Bash

# Navigate to the backend folder
cd resume-backend/tailor-api

# Build the project
mvn clean install
Python Script

Navigate to src/main/resources/scripts/.

Install the required library: pip install google-generativeai.

Open tailor.py and add your Gemini API key.

Frontend (React)

Bash

# Navigate to the frontend folder
cd frontend

# Install dependencies
npm install
Running the Application
Run the Spring Boot application.

In a separate terminal, start the React development server:

Bash

# From the /frontend directory
npm run dev
Open http://localhost:5173 in your browser.
