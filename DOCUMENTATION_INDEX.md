# Documentation Index

Welcome to the Visa Dispute Agent documentation! This index will help you find the right document for your needs.

## 🚀 Getting Started

**New to the project?** Start here:

1. **[README.md](README.md)** - Project overview, features, and quick links
2. **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Understand the system architecture

## 📚 Documentation by Role

### For Developers

**Setting Up**
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [.env.example](.env.example) - Environment configuration template
- [pyproject.toml](pyproject.toml) - Dependencies and project metadata

**Understanding the Code**
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture with diagrams
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - What's been built
- [app/agents/dispute_graph.py](app/agents/dispute_graph.py) - Main workflow logic

**Testing**
- [TESTING.md](TESTING.md) - Complete testing guide
- [tests/](tests/) - Test suite (property, unit, integration)
- [scripts/run_tests.sh](scripts/run_tests.sh) - Test runner script

**Development Workflow**
- [Makefile](Makefile) - Common development commands
- [.pre-commit-config.yaml](.pre-commit-config.yaml) - Code quality hooks
- [alembic/](alembic/) - Database migrations

### For API Users

**API Reference**
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete API reference
- http://localhost:8000/docs - Interactive Swagger UI (when running)
- http://localhost:8000/redoc - Alternative API docs (when running)

**Integration**
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Webhook integration guide
- [.env.example](.env.example) - Configuration options

### For DevOps/SRE

**Deployment**
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide
- [docker-compose.yml](docker-compose.yml) - Local infrastructure
- [Dockerfile](Dockerfile) - Production container image

**Database**
- [alembic/](alembic/) - Database migrations
- [app/db/schema.sql](app/db/schema.sql) - Database schema
- [scripts/seed_chromadb.py](scripts/seed_chromadb.py) - Vector store seeding

**Monitoring**
- [DEPLOYMENT.md](DEPLOYMENT.md) - Monitoring section
- [app/api/main.py](app/api/main.py) - Health check endpoint

### For Project Managers

**Status & Progress**
- [PROJECT_COMPLETION_REPORT.md](PROJECT_COMPLETION_REPORT.md) - Comprehensive completion report
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Current implementation status
- [.kiro/specs/visa-dispute-agent/tasks.md](.kiro/specs/visa-dispute-agent/tasks.md) - Task checklist

**Requirements & Design**
- [.kiro/specs/visa-dispute-agent/requirements.md](.kiro/specs/visa-dispute-agent/requirements.md) - Requirements specification
- [.kiro/specs/visa-dispute-agent/design.md](.kiro/specs/visa-dispute-agent/design.md) - Design document

## 📖 Documentation by Topic

### Architecture & Design

| Document | Description | Audience |
|----------|-------------|----------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture with Mermaid diagrams | Developers, Architects |
| [.kiro/specs/visa-dispute-agent/design.md](.kiro/specs/visa-dispute-agent/design.md) | Detailed design specification | Developers, Architects |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | What's been implemented | All |

### Setup & Configuration

| Document | Description | Audience |
|----------|-------------|----------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide | Developers |
| [.env.example](.env.example) | Environment variables | Developers, DevOps |
| [docker-compose.yml](docker-compose.yml) | Local infrastructure | Developers |

### API & Integration

| Document | Description | Audience |
|----------|-------------|----------|
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete API reference | API Users, Developers |
| [app/schema/models.py](app/schema/models.py) | Data models and schemas | Developers |

### Testing & Quality

| Document | Description | Audience |
|----------|-------------|----------|
| [TESTING.md](TESTING.md) | Testing strategy and guide | Developers, QA |
| [tests/](tests/) | Test suite | Developers |
| [.pre-commit-config.yaml](.pre-commit-config.yaml) | Code quality hooks | Developers |

### Deployment & Operations

| Document | Description | Audience |
|----------|-------------|----------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment guide | DevOps, SRE |
| [Dockerfile](Dockerfile) | Container image | DevOps |
| [Makefile](Makefile) | Build and deployment commands | Developers, DevOps |

### Project Management

| Document | Description | Audience |
|----------|-------------|----------|
| [PROJECT_COMPLETION_REPORT.md](PROJECT_COMPLETION_REPORT.md) | Comprehensive completion report | Managers, Stakeholders |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Current status | Managers |
| [.kiro/specs/visa-dispute-agent/requirements.md](.kiro/specs/visa-dispute-agent/requirements.md) | Requirements | All |

## 🔍 Quick Reference

### Common Tasks

**I want to...**

- **Get started quickly** → [QUICKSTART.md](QUICKSTART.md)
- **Understand the architecture** → [ARCHITECTURE.md](ARCHITECTURE.md)
- **Use the API** → [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Run tests** → [TESTING.md](TESTING.md)
- **Deploy to production** → [DEPLOYMENT.md](DEPLOYMENT.md)
- **Check project status** → [PROJECT_COMPLETION_REPORT.md](PROJECT_COMPLETION_REPORT.md)
- **See what's been built** → [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Understand requirements** → [.kiro/specs/visa-dispute-agent/requirements.md](.kiro/specs/visa-dispute-agent/requirements.md)

### Key Files

**Configuration**
- `.env.example` - Environment variables template
- `pyproject.toml` - Python dependencies
- `alembic.ini` - Database migration config
- `docker-compose.yml` - Local infrastructure

**Code Entry Points**
- `app/api/main.py` - FastAPI server
- `app/agents/dispute_graph.py` - LangGraph workflow
- `app/tools/rag_retriever.py` - RAG system
- `app/tools/transaction_enrichment.py` - Fraud detection

**Database**
- `app/db/schema.sql` - PostgreSQL schema
- `alembic/versions/001_initial_schema.py` - Initial migration
- `scripts/seed_chromadb.py` - Vector store seeding

**Testing**
- `tests/property_tests/` - Property-based tests
- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests
- `scripts/run_tests.sh` - Test runner

## 📊 Documentation Statistics

- **Total Documents**: 10 main documents
- **Total Pages**: 30+ pages of documentation
- **Code Files**: 25+ Python files
- **Test Files**: 12 test files
- **Configuration Files**: 8 config files

## 🎯 Documentation Quality

✅ **Complete** - All major topics covered  
✅ **Comprehensive** - Detailed explanations with examples  
✅ **Up-to-date** - Reflects current implementation  
✅ **Well-organized** - Easy to navigate  
✅ **Multi-audience** - Serves developers, users, and managers

## 📝 Contributing to Documentation

When updating documentation:

1. **Keep it current** - Update docs when code changes
2. **Be clear** - Use simple language and examples
3. **Be comprehensive** - Cover all aspects
4. **Be consistent** - Follow existing style
5. **Test examples** - Ensure code examples work

## 🆘 Getting Help

**Can't find what you need?**

1. Check this index for the right document
2. Use your editor's search (Cmd/Ctrl+F) within documents
3. Review the [README.md](README.md) for quick links
4. Check the [QUICKSTART.md](QUICKSTART.md) for common tasks

**Found an issue?**

- Documentation errors or outdated information
- Missing examples or unclear explanations
- Broken links or formatting issues

Please report issues or contribute improvements!

## 📚 External Resources

**Technologies Used**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [AsyncPG Documentation](https://magicstack.github.io/asyncpg/)

**Best Practices**
- [Property-Based Testing Guide](https://hypothesis.works/articles/what-is-property-based-testing/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Python Async Best Practices](https://docs.python.org/3/library/asyncio.html)

---

**Last Updated**: November 28, 2025  
**Version**: 1.0  
**Status**: Complete
