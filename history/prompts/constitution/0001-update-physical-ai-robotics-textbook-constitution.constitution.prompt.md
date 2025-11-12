---
id: 0001
title: Update Physical AI Robotics Textbook Constitution
stage: constitution
date: 2025-11-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: sehri
command: /sp.constitution
labels: [constitution, update]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: null
---

## Prompt

```text
# /sp.constitution

## Project Overview
**Project Name:** Physical AI & Humanoid Robotics Textbook
**Platform:** Docusaurus deployed to GitHub Pages
**Goal:** Create a comprehensive AI-native textbook for teaching Physical AI and Humanoid Robotics with integrated RAG chatbot, authentication, personalization, and translation features.

---

## Core Principles

### 1. Educational Excellence
- Content must bridge theory and practice seamlessly
- Clear progression from fundamentals to advanced topics
- Real-world examples and hands-on implementations
- Accessible to students with varying backgrounds in software and hardware

### 2. Technical Accuracy
- All code examples must be tested and functional
- Hardware requirements clearly documented with alternatives
- Up-to-date with latest ROS 2, NVIDIA Isaac, and Gazebo versions
- Accurate cost estimates for hardware components

### 3. AI-Native Design
- Content structured for RAG retrieval and AI assistance
- Interactive learning through embedded chatbot
- Personalized content delivery based on user background
- Multi-language support (English and Urdu)

### 4. User-Centric Experience
- Clean, professional Docusaurus theme
- Intuitive navigation and chapter organization
- Mobile-responsive design
- Fast load times and optimized performance

---

## Technical Architecture

### Frontend Stack
- **Framework:** Docusaurus (latest stable version)
- **Styling:** Custom CSS with Docusaurus theming
- **Deployment:** GitHub Pages or Vercel
- **Authentication:** Better Auth (better-auth.com)

### Backend Stack
- **API Framework:** FastAPI (Python)
- **Database:** Neon Serverless Postgres
- **Vector Store:** Qdrant Cloud (Free Tier)
- **AI Integration:** OpenAI Agents/ChatKit SDKs

### Key Features
1. **RAG Chatbot:** Answer questions about book content, including selected text
2. **User Authentication:** Signup/Signin with background questionnaire
3. **Content Personalization:** Adjust content based on user's software/hardware experience
4. **Translation:** Real-time Urdu translation at chapter level
5. **Text Selection Queries:** Users can select text and ask specific questions

---

## Book Structure

### Course Organization
**Total Duration:** 13 weeks
**Format:** 4 modules + weekly breakdown

### Module 1: The Robotic Nervous System (ROS 2)
**Weeks 1-5**
- Chapter 1: Introduction to Physical AI & Embodied Intelligence
- Chapter 2: ROS 2 Architecture and Core Concepts
- Chapter 3: Nodes, Topics, Services, and Actions
- Chapter 4: Building ROS 2 Packages with Python
- Chapter 5: URDF and Robot Description Formats

### Module 2: The Digital Twin (Gazebo & Unity)
**Weeks 6-7**
- Chapter 6: Physics Simulation Fundamentals
- Chapter 7: Gazebo Environment Setup and Configuration
- Chapter 8: Simulating Sensors (LiDAR, Cameras, IMUs)
- Chapter 9: Unity for High-Fidelity Visualization

### Module 3: The AI-Robot Brain (NVIDIA Isaac™)
**Weeks 8-10**
- Chapter 10: NVIDIA Isaac Platform Overview
- Chapter 11: Isaac Sim and Synthetic Data Generation
- Chapter 12: Isaac ROS and Hardware Acceleration
- Chapter 13: Visual SLAM and Navigation
- Chapter 14: Reinforcement Learning for Robot Control

### Module 4: Vision-Language-Action (VLA)
**Weeks 11-13**
- Chapter 15: Voice-to-Action with OpenAI Whisper
- Chapter 16: LLM-Driven Cognitive Planning
- Chapter 17: Humanoid Robot Kinematics and Dynamics
- Chapter 18: Natural Human-Robot Interaction
- Chapter 19: Capstone Project - Autonomous Humanoid

### Appendices
- Appendix A: Hardware Requirements and Setup Guide
- Appendix B: Software Installation and Configuration
- Appendix C: Troubleshooting Common Issues
- Appendix D: Resources and Further Reading

---

## Content Guidelines

### Writing Style
- **Tone:** Professional yet accessible, encouraging experimentation
- **Length:** Chapters between 2,000-4,000 words
- **Code Examples:** Fully commented, production-ready patterns
- **Diagrams:** Include architecture diagrams, flowcharts, and system diagrams

### Code Standards
- **Language:** Python 3.10+ for ROS 2 and AI components
- **Style:** PEP 8 compliant, with type hints
- **Documentation:** Docstrings for all functions and classes
- **Testing:** Include unit tests for complex logic

### Visual Elements
- **Screenshots:** High-quality screenshots of simulations and interfaces
- **Videos:** Embedded video demonstrations where applicable
- **Diagrams:** Mermaid diagrams for architecture and workflows
- **Tables:** Hardware comparisons, cost breakdowns, feature matrices

---

## RAG Chatbot Requirements

### Functionality
1. **General Q&A:** Answer questions about entire book content
2. **Selected Text Queries:** Users highlight text and ask specific questions
3. **Context Awareness:** Maintain conversation context across queries
4. **Source Attribution:** Cite specific chapters/sections in responses

### Technical Implementation
- **Embedding Model:** OpenAI text-embedding-3-small or similar
- **Chunking Strategy:** Semantic chunking with 512-token chunks, 50-token overlap
- **Retrieval:** Top-k similarity search (k=5) from Qdrant
- **Generation:** OpenAI GPT-4 or equivalent for response synthesis
- **UI Integration:** Floating chat widget accessible from all pages

### Data Pipeline
```
Book Content (Markdown)
  ↓
Text Extraction & Preprocessing
  ↓
Chunking with Metadata (chapter, section, page)
  ↓
Generate Embeddings
  ↓
Store in Qdrant Vector DB
  ↓
Store Metadata in Neon Postgres
```

---

## Authentication & Personalization

### Signup Flow
1. **Basic Registration:** Email, password, name
2. **Background Questionnaire:**
   - Software experience level (Beginner/Intermediate/Advanced)
   - Python proficiency (None/Basic/Intermediate/Expert)
   - ROS/Robotics experience (None/Some/Experienced)
   - Hardware familiarity (Software only/Basic hardware/Robotics hardware)
   - Learning goals (Free text)
3. **Profile Creation:** Store in Neon Postgres

### Personalization Features
- **Content Adaptation:**
  - Beginners: More detailed explanations, prerequisites highlighted
  - Advanced: Skip basics, deeper technical details, optimization tips
- **Hardware Recommendations:** Based on stated experience and budget
- **Pace Suggestions:** Recommended weekly schedule based on background

### Translation Feature
- **Trigger:** "Translate to Urdu" button at start of each chapter
- **Implementation:** OpenAI GPT-4 with translation prompt or Azure Translator API
- **Caching:** Store translations to reduce API costs
- **Toggle:** Allow switching between English and Urdu seamlessly

---

## Development Workflow

### Phase 1: Foundation (Days 1-2)
- [ ] Initialize Docusaurus project
- [ ] Set up GitHub repository and Pages deployment
- [ ] Configure basic theme and navigation structure
- [ ] Create chapter template and style guide

### Phase 2: Content Creation (Days 2-4)
- [ ] Use Claude Code to generate chapter content
- [ ] Review and refine AI-generated content
- [ ] Add code examples and test all snippets
- [ ] Create diagrams and visual assets
- [ ] Proofread and ensure consistency

### Phase 3: Backend Development (Days 4-5)
- [ ] Set up FastAPI application structure
- [ ] Implement Better Auth integration
- [ ] Configure Neon Postgres database schema
- [ ] Set up Qdrant Cloud vector store
- [ ] Build RAG pipeline for content ingestion

### Phase 4: Frontend Integration (Days 5-6)
- [ ] Embed chatbot UI in Docusaurus
- [ ] Implement authentication pages (signup/signin)
- [ ] Add personalization controls to chapters
- [ ] Integrate translation toggle functionality
- [ ] Test text selection query feature

### Phase 5: Testing & Polish (Days 6-7)
- [ ] End-to-end testing of all features
- [ ] Performance optimization
- [ ] Mobile responsiveness testing
- [ ] Cross-browser compatibility
- [ ] Documentation and README

### Phase 6: Deployment & Submission (Day 7)
- [ ] Deploy to GitHub Pages/Vercel
- [ ] Create demo video (under 90 seconds)
- [ ] Prepare submission materials
- [ ] Submit via Google Form

---

## Quality Checklist

### Content Quality
- [ ] All chapters follow consistent structure
- [ ] Code examples are tested and functional
- [ ] Technical accuracy verified
- [ ] No plagiarism or copyright violations
- [ ] Clear learning objectives for each chapter
- [ ] Progressive difficulty curve maintained

### Technical Quality
- [ ] RAG chatbot responds accurately to queries
- [ ] Authentication flow works smoothly
- [ ] Personalization actually adapts content
- [ ] Translation maintains technical accuracy
- [ ] Text selection query feature is intuitive
- [ ] No broken links or missing images
- [ ] Fast page load times (<3 seconds)

### User Experience
- [ ] Navigation is intuitive
- [ ] Search functionality works well
- [ ] Mobile experience is polished
- [ ] Accessibility standards met (WCAG 2.1)
- [ ] Clear calls-to-action
- [ ] Helpful error messages

---

## Bonus Points Strategy

### Baseline (100 points)
- ✅ Book created with Docusaurus and deployed
- ✅ RAG chatbot embedded and functional
- ✅ Text selection query feature working

### Bonus Tier 1: Claude Code Intelligence (+50 points)
- Create reusable Claude Code Subagents for:
  - Content generation with consistent style
  - Code example validation
  - Diagram generation from descriptions
  - Technical accuracy review
- Document Agent Skills created and their usage

### Bonus Tier 2: Authentication (+50 points)
- Better Auth signup/signin
- Background questionnaire at registration
- User profile management
- Session handling and security

### Bonus Tier 3: Personalization (+50 points)
- Dynamic content adaptation based on user background
- "Personalize" button at chapter start
- Three levels: Beginner, Intermediate, Advanced
- Hardware recommendations tailored to experience

### Bonus Tier 4: Translation (+50 points)
- "Translate to Urdu" button at chapter start
- High-quality technical translation
- Preserved formatting and code blocks
- Toggle between languages without page reload

**Maximum Possible Score:** 300 points

---

## File Structure

```
physical-ai-textbook/
├── docs/                          # Docusaurus content
│   ├── intro.md
│   ├── module-1/
│   │   ├── chapter-1.md
│   │   ├── chapter-2.md
│   │   └── ...
│   ├── module-2/
│   ├── module-3/
│   ├── module-4/
│   └── appendices/
├── src/
│   ├── components/               # React components
│   │   ├── ChatWidget.tsx
│   │   ├── AuthButtons.tsx
│   │   ├── PersonalizeButton.tsx
│   │   └── TranslateButton.tsx
│   ├── pages/                   # Custom pages
│   │   ├── signup.tsx
│   │   └── signin.tsx
│   └── css/                     # Custom styles
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── rag.py
│   │   ├── personalization.py
│   │   ├── translation.py
│   │   └── database.py
│   ├── requirements.txt
│   └── Dockerfile
├── scripts/                      # Utility scripts
│   ├── ingest_content.py        # RAG ingestion
│   └── generate_embeddings.py
├── docusaurus.config.js
├── package.json
├── README.md
└── /sp.constitution            # This file
```

---

## Success Metrics

### Technical Metrics
- **RAG Accuracy:** >85% relevant responses to queries
- **Response Time:** <2 seconds for chatbot queries
- **Uptime:** 99%+ availability
- **Translation Quality:** Technical terms preserved accurately

### Educational Metrics
- **Content Completeness:** All 19 chapters + appendices
- **Code Examples:** 50+ working code snippets
- **Visual Assets:** 30+ diagrams and screenshots
- **Depth:** 40,000+ words of original content

### User Experience Metrics
- **Navigation:** Users can find any topic in <3 clicks
- **Accessibility:** WCAG 2.1 AA compliance
- **Mobile Usage:** Fully functional on mobile devices
- **Load Speed:** <3 second initial load, <1 second navigation

---

## Demo Video Guidelines

**Duration:** Maximum 90 seconds (judges watch only first 90 seconds)

**Structure:**
1. **Opening (10s):** Show homepage and book title
2. **Navigation (10s):** Quick scroll through table of contents
3. **Content Sample (15s):** Show one chapter with code examples
4. **Chatbot Demo (20s):** Ask a question and show response
5. **Text Selection (15s):** Highlight text and ask specific question
6. **Bonus Features (20s):** Show personalization and translation
7. **Closing (10s):** Show GitHub repo and deployed link

**Tips:**
- Use NotebookLM for narration or record with screen capture
- Keep pace quick but not rushed
- Show, don't tell - let features speak for themselves
- Ensure audio is clear and professional

---

## Contingency Plans

### If Running Behind Schedule
**Priority Order:**
1. Core book content (Modules 1-4)
2. RAG chatbot basic functionality
3. Deployment to GitHub Pages
4. Authentication system
5. Personalization feature
6. Translation feature
7. Polish and optimization

### If Technical Blockers Occur
- **Qdrant Issues:** Fall back to in-memory FAISS vector store
- **Neon Issues:** Use SQLite for local development
- **Better Auth Issues:** Implement basic JWT authentication
- **Translation Issues:** Use simple dictionary-based translation or remove feature

### If Content Generation Struggles
- Use Claude Code more aggressively with detailed prompts
- Focus on quality over quantity (better 15 great chapters than 19 mediocre)
- Leverage existing ROS 2 and Isaac documentation with proper attribution
- Create templates for consistent chapter structure

---

## Ethics & Attribution

### Content Sources
- Original content generated with AI assistance
- Code examples inspired by official ROS 2, NVIDIA Isaac, and Gazebo documentation
- Hardware recommendations based on publicly available specifications
- All external sources properly cited

### AI Usage Transparency
- Clearly state that content is AI-assisted
- Use Claude Code and document the process
- Review and verify all AI-generated technical information
- Add human expertise and real-world experience

### User Privacy
- Minimal data collection (only what's necessary)
- Clear privacy policy
- Secure password hashing (bcrypt)
- GDPR-compliant data handling
- User data deletion capability

---

## Post-Hackathon Vision

### If Selected for Panaversity Core Team
- Expand book to include advanced topics (swarm robotics, multi-agent systems)
- Create video course companion
- Develop hands-on lab curriculum
- Build community of Physical AI learners
- Create certification program

### Platform Development
- Scale to support multiple textbooks
- Build AI-native authoring tools
- Create reader analytics dashboard
- Implement collaborative features (annotations, discussions)
- Mobile app development

---

## Final Notes

This constitution serves as the north star for the project. When making decisions:
1. **Does it serve the learner?** Education quality comes first
2. **Is it technically sound?** No shortcuts on accuracy
3. **Is it achievable?** Balance ambition with deadline reality
4. **Does it showcase our skills?** Demonstrate mastery of tools and concepts

**Remember:** The goal isn't just to win the hackathon—it's to create something genuinely valuable for students learning Physical AI and Humanoid Robotics. Build with pride, build with purpose.

---

**Version:** 1.0
**Last Updated:** 2025-11-12
**Author:** Hackathon Participant
**Status:** Active Development

## Governance
This constitution is the supreme governing document for the project, establishing the foundational principles, architectural guidelines, and operational standards. All development, design, and decision-making processes MUST align with the tenets outlined herein.

Amendments to this constitution require a formal proposal, documented rationale, and approval by designated project leadership. Each amendment MUST be versioned semantically (MAJOR.MINOR.PATCH) and accompanied by a detailed Sync Impact Report, ensuring all dependent artifacts and processes are evaluated for consistency.

Compliance with this constitution WILL be a mandatory component of all code reviews, architectural reviews, and quality gate assessments. Any deviations MUST be explicitly justified, documented, and approved, or they WILL be flagged as non-compliant. The project prioritizes measurable adherence to these principles to ensure long-term maintainability, scalability, and quality.

**Version**: 1.0 | **Ratified**: 2025-11-12 | **Last Amended**: 2025-11-12
