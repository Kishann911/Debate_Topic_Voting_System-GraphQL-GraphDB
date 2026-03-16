# 🗳️ Debate Topic Voting System
### Modern GraphQL API with FastAPI & SQLAlchemy

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![GraphQL](https://img.strawberry.rocks/badge/v1/strawberry-graphql.svg)](https://strawberry.rocks/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)

A high-performance, **frontend-less** GraphQL API designed for educational environments. This system allows students to vote on debate topics while ensuring data integrity and real-time result aggregation.

---

## ✨ Key Features

- 🚀 **Lightning Fast**: Built on FastAPI and Uvicorn for ultra-low latency.
- 🧬 **Flexible Schema**: GraphQL-powered querying for precise data retrieval.
- 🛡️ **Vote Integrity**: Built-in duplicate prevention (single vote per student).
- 📊 **Real-time Analytics**: Immediate vote count calculation and topic ranking.
- 🔄 **Round Tracking**: Manage multi-stage debate rounds seamlessly.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **API Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Query Language** | [Strawberry GraphQL](https://strawberry.rocks/) |
| **ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) |
| **Database** | SQLite (Production-ready local storage) |
| **Server** | Uvicorn (ASGI) |

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.13+ installed.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Kishann911/Debate_Topic_Voting_System-GraphQL-GraphDB.git
cd Debate_Topic_Voting_System-GraphQL-GraphDB

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the API
```bash
# Launch the server
python main.py
```
The API will be available at `http://localhost:8000/graphql`

---

## 🔍 Example Usage

### Fetch Topics (Ranked by Votes)
```graphql
query {
  topics(category: "social") {
    id
    title
    totalVotes
  }
}
```

### Cast a Vote
```graphql
mutation {
  castTopicVote(input: {
    studentId: 101,
    topicId: 1
  }) {
    vote { id }
    error
  }
}
```

---

## 📜 Database Schema

The system implements five core models:
- **Student**: Identity management.
- **Topic**: Debate subjects (Categories: `social`, `political`).
- **Vote**: Transaction log of all entries.
- **Result**: View-optimized vote tallies.
- **Round**: Debate progression tracking.

---

## 🎨 Professional Design
*This project focuses on a lean, scalable backend architecture, optimized for integration with modern React/Next.js frontends or direct API consumption.*

---
Developed by **Kishan** 🚀
