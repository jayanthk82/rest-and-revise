# RecallX - AI-Powered Personalized Learning Path Generator

## Stop Forgetting, Start Achieving.

RecallX is a smart revision tool that creates a personalized learning journey for every student. By tracking your learning, identifying knowledge gaps, and suggesting what to revise and when, RecallX helps you retain information longer and achieve your career goals faster.

This project was developed for the Smart India Hackathon 2025.

### The Problem We Solve

  - **Students forget most of what they study** in a short amount of time.
  - **Generic learning paths waste time** and don't prepare students for real-world jobs.
  - There's **no system to tell you when and what to revise**.
  - **Skills learned aren't connected to actual job needs**.

### Our Innovative Solution

RecallX is a revolutionary platform that tackles these challenges head-on. Here’s how:

  - **Smart Revision Tool**: Our intelligent system reminds you of the right topics at the right time.
  - **Skill Extraction**: We extract skills from every learning activity, from solving a coding problem to uploading your notes.
  - **Dynamic Skill Profiles**: RecallX creates a living, breathing profile of your skills that's always up-to-date.
  - **Tailored Learning Journey**: We generate a personalized learning path that combines revision with new topics aligned with your goals.
  - **Personalized Job Recommendations**: Get job suggestions and courses tailored to your unique skill profile.

### How It Works

1.  **Upload Anything**: Learners can upload notes, problems they've solved, or answers they've written.
2.  **System Analysis**: Our system tags concepts and extracts relevant skills from the uploaded content.
3.  **Forgetting Curve Application**: We apply the forgetting curve principle to determine what you need to revise each day.
4.  **Knowledge Gap Identification**: The system identifies your weak areas and integrates them into your revision plan.
5.  **New Learning Path Creation**: A curated learning path is generated just for you.
6.  **Stay on Track**: Receive reminders and recommendations via your dashboard or email.

### Personalized Skill Path

  - **From Learning to Earning**: We bridge the gap between what you learn and what employers are looking for.
  - **Example**: If you solve a problem on "SQL joins," we add "SQL" and "Databases" to your skill profile.
  - **Career Mapping**: The tool maps your skill profile against the requirements for various job roles.
  - **Upskilling Suggestions**: If you have missing skills, we suggest NCVET qualifications and NSQF-based training programs.

### Technical Approach

  - **Backend**: Django and Django REST Framework are used to build our powerful REST APIs.
  - **Frontend**: A user-friendly interface built with modern frontend technologies.
  - **Database**: We use a local Postgres database for robust data storage.
  - **Background Jobs**: Celery and Redis are used for background tasks like sending revision reminders and newsletters.
  - **Integrations and APIs**:
      - **Retool**: Dashboards for learners, trainers, and policymakers.
      - **Email/Newsletter**: Automated nudges and updates to keep you on track.
      - **Job Suggestions API**: Live job openings to help you find your dream job.
      - **Resume Builder**: Automatically generate a resume from your skill profile.

### Getting Started

To run the project in a virtual environment, follow these steps:

1.  **Run the Django server**:
    ```bash
    python manage.py runserver
    ```
2.  **Run the Celery worker**:
    ```bash
    celery -A backend worker --loglevel=info
    ```
3.  **Run the Celery beat scheduler**:
    ```bash
    celery -A backend beat --loglevel=INFO
    ```
4.  **Start the Redis server**:
    ```bash
    docker start my-redis-mailbox
    ```

### Impact

  - **For Students**:
      - Better knowledge retention.
      - Personalized skill journey aligned with career goals.
      - Increased confidence with a clear view of progress.
  - **For Teachers**:
      - Real-time visibility into student retention.
      - Ability to track skill growth and gaps.
      - Data-driven insights for better mentoring.
  - **For Industry**:
      - Access to job-ready candidates with verified skill profiles.
      - Faster and more efficient hiring process.
      - Reduced cost of retraining freshers.
