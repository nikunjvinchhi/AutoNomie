# AutoNomie Frontend - Spec Agent Testing Interface

A sophisticated chat + forms interface for testing the AutoNomie Spec Agent.

## Design Philosophy: Editorial Tech
- **Typography**: Crimson Pro (serif headlines) + Inter Tight (clean body text)
- **Colors**: Sophisticated neutrals with electric blue accents
- **Layout**: Magazine-style content blocks with smart contextual forms
- **UX**: Professional consultation experience with natural conversation flow

## Features

✨ **Natural Conversation Interface**
- Real-time chat with the Spec Agent AI
- Message history and timestamps
- Typing indicators and smooth animations

📋 **Smart Contextual Forms**
- Forms appear automatically based on conversation context
- Project type selection, priority setting, tech preferences
- Structured data collection when needed

📊 **Progress Tracking**
- Visual progress bar showing requirement gathering completion
- Phase indicators (Discovery → Core Requirements → Follow-up → Validation)
- Real-time conversation state management

📱 **Responsive Design**
- Mobile-friendly interface
- Touch-optimized inputs and buttons
- Adaptive layout for all screen sizes

## Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm start
```

The app will open at http://localhost:3000 and automatically proxy API calls to http://localhost:8000

### 3. Start the Backend
In another terminal, ensure your AutoNomie API is running:
```bash
# From the root directory
docker-compose up -d
# OR
source venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

## Testing Workflow

1. **Project Setup**: Enter project name, your name, and brief description
2. **AI Conversation**: Natural chat with the Spec Agent
3. **Smart Forms**: Contextual forms appear for structured data
4. **Progress Tracking**: Watch completion percentage increase
5. **Full Transcript**: Review complete conversation history

## API Integration

The frontend connects to these AutoNomie API endpoints:
- `POST /projects/` - Create new project
- `POST /spec-agent/conversations/` - Start conversation
- `POST /spec-agent/conversations/{id}/messages/` - Send messages
- `GET /spec-agent/conversations/{id}/` - Get conversation status

## Building for Production

```bash
npm run build
```

Creates optimized production build in the `build/` directory.

## Client Demo Ready

This interface is designed for **real client testing**:
- Professional appearance builds trust
- Natural conversation flow keeps clients engaged
- Smart forms prevent information gaps
- Progress tracking shows clear advancement
- Mobile-friendly for use anywhere