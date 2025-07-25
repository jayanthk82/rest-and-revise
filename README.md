# Rest and Revise

A Django REST API service for text summarization using AI models.

## Project Overview

This project provides an API endpoint for summarizing text content, designed to help with creating revision newsletters and study materials.

## Branch Structure

- **main** - Primary development branch (default)
- **feature/backend-setup** - Initial backend setup (merged to main)

## Quick Start

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install django openai python-dotenv
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Add your OPENROUTER_API_KEY to .env
   ```

4. Run the development server:
   ```bash
   python manage.py check
   python manage.py runserver
   ```

## API Endpoints

### POST /api/summarize/
Summarizes the provided text content.

**Request:**
```json
{
  "fileContent": "Your text content to summarize"
}
```

**Response:**
```json
{
  "summary": "Summarized text",
  "originalWordCount": 150,
  "summaryWordCount": 50
}
```

## Development

This project follows standard Django development practices. The main branch contains the latest stable code and is the default branch for all development work.

## Contributing

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Submit a pull request to `main`