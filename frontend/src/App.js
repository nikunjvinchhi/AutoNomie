import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MessageCircle,
  Send,
  User,
  Bot,
  CheckCircle,
  Circle,
  ArrowRight,
  Sparkles,
  FileText,
  Clock,
  Target
} from 'lucide-react';
import './App.css';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL ||
  (process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : '');

const App = () => {
  const [project, setProject] = useState(null);
  const [conversation, setConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState('project');
  const [showSmartForm, setShowSmartForm] = useState(false);
  const [smartFormData, setSmartFormData] = useState({});
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const createProject = async (projectData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/projects/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(projectData)
      });
      return await response.json();
    } catch (error) {
      console.error('Error creating project:', error);
      return null;
    }
  };

  const startConversation = async (projectId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/spec-agent/conversations/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_id: projectId,
          client_info: { name: 'Client User' },
          project_type_hint: 'web_application'
        })
      });
      return await response.json();
    } catch (error) {
      console.error('Error starting conversation:', error);
      return null;
    }
  };

  const sendMessage = async (message) => {
    if (!conversation) return;

    setIsLoading(true);
    const newMessage = { text: message, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, newMessage]);

    try {
      const response = await fetch(`${API_BASE_URL}/spec-agent/conversations/${conversation.conversation_id}/messages/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message_text: message,
          sender_type: 'client'
        })
      });

      const data = await response.json();

      const aiMessage = {
        text: data.ai_response,
        sender: 'ai',
        timestamp: new Date(),
        conversationState: data.conversation_state,
        nextQuestion: data.next_question
      };

      setMessages(prev => [...prev, aiMessage]);

      // Trigger smart form for certain phases or keywords
      if (data.conversation_state?.current_phase === 'core_requirements' ||
          data.ai_response.toLowerCase().includes('project type') ||
          data.ai_response.toLowerCase().includes('technology')) {
        setTimeout(() => setShowSmartForm(true), 1000);
      }

    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleProjectSetup = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const projectData = {
      name: formData.get('projectName'),
      description: formData.get('projectDescription'),
      client_info: formData.get('clientName')
    };

    const newProject = await createProject(projectData);
    if (newProject) {
      setProject(newProject);
      const newConversation = await startConversation(newProject.id);
      if (newConversation) {
        setConversation(newConversation);
        setMessages([{
          text: newConversation.initial_message,
          sender: 'ai',
          timestamp: new Date()
        }]);
        setCurrentStep('conversation');
      }
    }
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      sendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  const handleSmartFormSubmit = (data) => {
    setSmartFormData(prev => ({ ...prev, ...data }));
    setShowSmartForm(false);

    // Send structured response back to the agent
    const structuredMessage = Object.entries(data)
      .map(([key, value]) => `${key}: ${value}`)
      .join(', ');
    sendMessage(`Based on the form: ${structuredMessage}`);
  };

  return (
    <div className="app">
      <Header />

      <main className="main-content">
        {currentStep === 'project' && (
          <ProjectSetup onSubmit={handleProjectSetup} />
        )}

        {currentStep === 'conversation' && (
          <>
            <ConversationHeader
              project={project}
              conversationState={messages[messages.length - 1]?.conversationState}
            />
            <ChatInterface
              messages={messages}
              inputValue={inputValue}
              setInputValue={setInputValue}
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              messagesEndRef={messagesEndRef}
            />
          </>
        )}
      </main>

      <AnimatePresence>
        {showSmartForm && (
          <SmartForm
            onSubmit={handleSmartFormSubmit}
            onClose={() => setShowSmartForm(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

const Header = () => (
  <motion.header
    className="header"
    initial={{ y: -20, opacity: 0 }}
    animate={{ y: 0, opacity: 1 }}
    transition={{ duration: 0.6 }}
  >
    <div className="header-content">
      <div className="logo">
        <Sparkles size={24} />
        <span>AutoNomie</span>
      </div>
      <div className="header-meta">
        <span className="phase-tag">Spec Agent</span>
        <span className="version">Alpha</span>
      </div>
    </div>
  </motion.header>
);

const ProjectSetup = ({ onSubmit }) => (
  <motion.section
    className="project-setup"
    initial={{ opacity: 0, y: 40 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.8, delay: 0.2 }}
  >
    <div className="setup-content">
      <div className="setup-header">
        <h1>Start Your Project</h1>
        <p>AutoNomie's Spec Agent will guide you through requirement gathering using AI-powered conversation and smart forms.</p>
      </div>

      <form onSubmit={onSubmit} className="setup-form">
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="projectName">Project Name</label>
            <input
              type="text"
              id="projectName"
              name="projectName"
              required
              placeholder="e.g., Task Management System"
            />
          </div>

          <div className="form-group">
            <label htmlFor="clientName">Your Name</label>
            <input
              type="text"
              id="clientName"
              name="clientName"
              required
              placeholder="e.g., Sarah Johnson"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="projectDescription">Brief Description</label>
          <textarea
            id="projectDescription"
            name="projectDescription"
            rows="3"
            placeholder="Tell us what you're trying to build in a few sentences..."
          />
        </div>

        <button type="submit" className="primary-button">
          <span>Begin Requirements Session</span>
          <ArrowRight size={18} />
        </button>
      </form>
    </div>
  </motion.section>
);

const ConversationHeader = ({ project, conversationState }) => {
  const progress = conversationState?.completion_percentage || 0;
  const phase = conversationState?.current_phase || 'introduction';

  const phaseLabels = {
    introduction: 'Discovery & Introduction',
    core_requirements: 'Core Requirements',
    adaptive_followup: 'Detailed Follow-up',
    validation: 'Requirements Validation'
  };

  return (
    <motion.div
      className="conversation-header"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="header-main">
        <div className="project-info">
          <h2>{project?.name}</h2>
          <p className="phase-label">{phaseLabels[phase] || phase}</p>
        </div>

        <div className="progress-section">
          <div className="progress-bar">
            <motion.div
              className="progress-fill"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 1 }}
            />
          </div>
          <span className="progress-text">{Math.round(progress)}% Complete</span>
        </div>
      </div>
    </motion.div>
  );
};

const ChatInterface = ({ messages, inputValue, setInputValue, onSendMessage, isLoading, messagesEndRef }) => (
  <div className="chat-interface">
    <div className="messages-container">
      <AnimatePresence>
        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))}
      </AnimatePresence>
      {isLoading && <LoadingIndicator />}
      <div ref={messagesEndRef} />
    </div>

    <form onSubmit={onSendMessage} className="message-input-form">
      <div className="input-container">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Share your thoughts, requirements, or questions..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          <Send size={18} />
        </button>
      </div>
    </form>
  </div>
);

const MessageBubble = ({ message }) => (
  <motion.div
    className={`message ${message.sender}`}
    initial={{ opacity: 0, y: 20, scale: 0.95 }}
    animate={{ opacity: 1, y: 0, scale: 1 }}
    transition={{ duration: 0.4 }}
  >
    <div className="message-avatar">
      {message.sender === 'user' ? <User size={16} /> : <Bot size={16} />}
    </div>
    <div className="message-content">
      <div className="message-text">{message.text}</div>
      <div className="message-time">
        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
    </div>
  </motion.div>
);

const LoadingIndicator = () => (
  <motion.div
    className="loading-indicator"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
  >
    <div className="loading-avatar">
      <Bot size={16} />
    </div>
    <div className="loading-dots">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </motion.div>
);

const SmartForm = ({ onSubmit, onClose }) => {
  const [formData, setFormData] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <motion.div
      className="smart-form-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="smart-form"
        initial={{ scale: 0.9, y: 40 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.9, y: 40 }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="smart-form-header">
          <h3>Quick Details</h3>
          <p>Help us understand your project better with these structured questions.</p>
        </div>

        <form onSubmit={handleSubmit} className="smart-form-content">
          <div className="form-section">
            <label>Project Type</label>
            <div className="radio-group">
              {['Web Application', 'Mobile App', 'API Service', 'Desktop App', 'Other'].map(option => (
                <label key={option} className="radio-option">
                  <input
                    type="radio"
                    name="projectType"
                    value={option}
                    onChange={(e) => setFormData(prev => ({ ...prev, projectType: e.target.value }))}
                  />
                  <span>{option}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="form-section">
            <label>Priority Level</label>
            <select
              onChange={(e) => setFormData(prev => ({ ...prev, priority: e.target.value }))}
              defaultValue=""
            >
              <option value="">Select priority...</option>
              <option value="high">High - Launch ASAP</option>
              <option value="medium">Medium - Next few months</option>
              <option value="low">Low - Future consideration</option>
            </select>
          </div>

          <div className="form-actions">
            <button type="button" onClick={onClose} className="secondary-button">
              Skip for now
            </button>
            <button type="submit" className="primary-button">
              Continue Conversation
            </button>
          </div>
        </form>
      </motion.div>
    </motion.div>
  );
};

export default App;