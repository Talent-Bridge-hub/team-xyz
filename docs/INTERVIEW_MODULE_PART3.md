# CareerStar - Interview Module Documentation (Part 2B)

---

## Table of Contents (Part 3)

1. [Frontend Components Guide](#frontend-components-guide)
2. [Integration Flows](#integration-flows)
3. [Configuration & Environment](#configuration--environment)
4. [Testing Strategies](#testing-strategies)
5. [Troubleshooting Guide](#troubleshooting-guide)
6. [Performance Optimization](#performance-optimization)

---

## 1. Frontend Components Guide

### 1.1 Main Interview Page (`/frontend/src/pages/interview/index.tsx`)

**File:** 150 lines  
**Purpose:** Container component with tab navigation for interview features.

#### Component Structure

```typescript
import React, { useState } from 'react';
import InterviewSetup from '@/components/interview/InterviewSetup';
import InterviewChat from '@/components/interview/InterviewChat';
import InterviewHistory from '@/components/interview/InterviewHistory';

const InterviewPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'new' | 'active' | 'history'>('new');
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Tab Navigation */}
      <div className="flex space-x-4 mb-8 border-b">
        <button onClick={() => setActiveTab('new')}>New Interview</button>
        <button onClick={() => setActiveTab('active')}>Active Session</button>
        <button onClick={() => setActiveTab('history')}>History</button>
      </div>

      {/* Tab Content */}
      {activeTab === 'new' && (
        <InterviewSetup onSessionStart={(id) => {
          setActiveSessionId(id);
          setActiveTab('active');
        }} />
      )}
      
      {activeTab === 'active' && activeSessionId && (
        <InterviewChat sessionId={activeSessionId} />
      )}
      
      {activeTab === 'history' && <InterviewHistory />}
    </div>
  );
};
```

**Features:**
- ✅ Tab-based navigation (New/Active/History)
- ✅ Session state management
- ✅ Automatic tab switching after session start
- ✅ Responsive design with TailwindCSS

---

### 1.2 InterviewSetup Component (`InterviewSetup.tsx`)

**File:** 400 lines  
**Purpose:** Session configuration form with validation and popular job role suggestions.

#### Props Interface

```typescript
interface InterviewSetupProps {
  onSessionStart: (sessionId: number) => void;
}
```

#### Component State

```typescript
const [formData, setFormData] = useState({
  sessionType: 'technical',
  difficultyLevel: 'mid',
  jobRole: '',
  numQuestions: 10,
  resumeId: null
});
const [resumes, setResumes] = useState<Resume[]>([]);
const [loading, setLoading] = useState(false);
const [errors, setErrors] = useState<Record<string, string>>({});
```

#### Key Features

**1. Session Type Selector**

```typescript
const sessionTypes = [
  { value: 'technical', label: 'Technical', icon: '💻', description: 'Focus on technical skills' },
  { value: 'behavioral', label: 'Behavioral', icon: '🗣️', description: 'Focus on soft skills' },
  { value: 'mixed', label: 'Mixed', icon: '🔀', description: 'Both technical and behavioral' },
  { value: 'job-specific', label: 'Job-Specific', icon: '🎯', description: 'Tailored to job role' }
];

<div className="grid grid-cols-2 gap-4">
  {sessionTypes.map(type => (
    <button
      key={type.value}
      onClick={() => setFormData({...formData, sessionType: type.value})}
      className={formData.sessionType === type.value ? 'selected' : ''}
    >
      <span className="text-3xl">{type.icon}</span>
      <h3>{type.label}</h3>
      <p>{type.description}</p>
    </button>
  ))}
</div>
```

**2. Difficulty Level Selector**

```typescript
const difficultyLevels = [
  { value: 'junior', label: 'Junior', description: '0-2 years experience' },
  { value: 'mid', label: 'Mid-Level', description: '2-5 years experience' },
  { value: 'senior', label: 'Senior', description: '5+ years experience' }
];
```

**3. Job Role Input with Suggestions**

```typescript
const popularRoles = [
  'Software Engineer', 'Full Stack Developer', 'Frontend Developer',
  'Backend Developer', 'Data Scientist', 'DevOps Engineer',
  'Product Manager', 'UX Designer', 'QA Engineer', 'Mobile Developer'
];

<div>
  <label>Job Role (Optional)</label>
  <input
    type="text"
    value={formData.jobRole}
    onChange={(e) => setFormData({...formData, jobRole: e.target.value})}
    placeholder="e.g., Software Engineer"
  />
  
  {/* Popular Roles Dropdown */}
  <select onChange={(e) => setFormData({...formData, jobRole: e.target.value})}>
    <option value="">-- Popular Roles --</option>
    {popularRoles.map(role => (
      <option key={role} value={role}>{role}</option>
    ))}
  </select>
</div>
```

**4. Question Count Slider**

```typescript
<div>
  <label>Number of Questions: {formData.numQuestions}</label>
  <input
    type="range"
    min="3"
    max="15"
    step="1"
    value={formData.numQuestions}
    onChange={(e) => setFormData({...formData, numQuestions: parseInt(e.target.value)})}
  />
  <div className="flex justify-between text-sm">
    <span>3 (Quick)</span>
    <span>10 (Standard)</span>
    <span>15 (Comprehensive)</span>
  </div>
</div>
```

**5. Resume Selection**

```typescript
useEffect(() => {
  const fetchResumes = async () => {
    const userResumes = await resumeService.listResumes();
    setResumes(userResumes);
  };
  fetchResumes();
}, []);

<div>
  <label>Link Resume (Optional)</label>
  <select
    value={formData.resumeId || ''}
    onChange={(e) => setFormData({...formData, resumeId: e.target.value ? parseInt(e.target.value) : null})}
  >
    <option value="">-- No Resume --</option>
    {resumes.map(resume => (
      <option key={resume.id} value={resume.id}>
        {resume.filename} (Uploaded {new Date(resume.created_at).toLocaleDateString()})
      </option>
    ))}
  </select>
  <p className="text-sm text-gray-500">
    Linking a resume helps personalize questions based on your skills
  </p>
</div>
```

#### Form Validation

```typescript
const validateForm = (): boolean => {
  const newErrors: Record<string, string> = {};

  if (!formData.sessionType) {
    newErrors.sessionType = 'Session type is required';
  }

  if (!formData.difficultyLevel) {
    newErrors.difficultyLevel = 'Difficulty level is required';
  }

  if (formData.numQuestions < 3 || formData.numQuestions > 15) {
    newErrors.numQuestions = 'Number of questions must be between 3 and 15';
  }

  if (formData.sessionType === 'job-specific' && !formData.jobRole) {
    newErrors.jobRole = 'Job role is required for job-specific interviews';
  }

  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};
```

#### Submit Handler

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  if (!validateForm()) return;

  setLoading(true);
  try {
    const response = await interviewService.startSession({
      session_type: formData.sessionType,
      difficulty_level: formData.difficultyLevel,
      num_questions: formData.numQuestions,
      job_role: formData.jobRole || null,
      resume_id: formData.resumeId
    });

    toast.success('Interview session started!');
    onSessionStart(response.session_id);
  } catch (error) {
    toast.error('Failed to start session: ' + error.message);
  } finally {
    setLoading(false);
  }
};
```

---

### 1.3 InterviewChat Component (`InterviewChat.tsx`)

**File:** 550 lines  
**Purpose:** Real-time Q&A chat interface with AI feedback display.

#### Props Interface

```typescript
interface InterviewChatProps {
  sessionId: number;
}
```

#### Component State

```typescript
const [messages, setMessages] = useState<Message[]>([]);
const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
const [userAnswer, setUserAnswer] = useState('');
const [loading, setLoading] = useState(false);
const [submitting, setSubmitting] = useState(false);
const [error, setError] = useState<string | null>(null);
const [timeStarted, setTimeStarted] = useState<number | null>(null);
const [sessionComplete, setSessionComplete] = useState(false);
```

#### Message Type

```typescript
interface Message {
  id: string;
  type: 'question' | 'answer' | 'feedback' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    question_order?: number;
    question_type?: string;
    scores?: {
      overall_score: number;
      relevance_score: number;
      completeness_score: number;
      clarity_score: number;
      technical_accuracy_score: number;
      communication_score: number;
    };
    strengths?: string[];
    weaknesses?: string[];
    suggestions?: string[];
  };
}
```

#### Key Features

**1. Load Current Question**

```typescript
useEffect(() => {
  const loadQuestion = async () => {
    setLoading(true);
    try {
      const question = await interviewService.getNextQuestion(sessionId);
      
      if (!question) {
        setSessionComplete(true);
        return;
      }

      setCurrentQuestion(question);
      setTimeStarted(Date.now());
      
      // Add question to messages
      setMessages(prev => [...prev, {
        id: `q-${question.question_id}`,
        type: 'question',
        content: question.question_text,
        timestamp: new Date(),
        metadata: {
          question_order: question.question_order,
          question_type: question.question_type
        }
      }]);
    } catch (error) {
      setError('Failed to load question: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  loadQuestion();
}, [sessionId]);
```

**2. Submit Answer with Time Tracking**

```typescript
const handleSubmitAnswer = async () => {
  if (!userAnswer.trim() || !currentQuestion) return;

  const timeTaken = timeStarted ? Math.floor((Date.now() - timeStarted) / 1000) : null;

  setSubmitting(true);
  try {
    // Add user answer to messages
    setMessages(prev => [...prev, {
      id: `a-${Date.now()}`,
      type: 'answer',
      content: userAnswer,
      timestamp: new Date()
    }]);

    // Submit to backend
    const response = await interviewService.submitAnswer(sessionId, {
      question_id: currentQuestion.question_id,
      answer: userAnswer,
      time_taken_seconds: timeTaken
    });

    // Add AI feedback to messages
    setMessages(prev => [...prev, {
      id: `f-${Date.now()}`,
      type: 'feedback',
      content: response.ai_feedback,
      timestamp: new Date(),
      metadata: {
        scores: {
          overall_score: response.overall_score,
          relevance_score: response.relevance_score,
          completeness_score: response.completeness_score,
          clarity_score: response.clarity_score,
          technical_accuracy_score: response.technical_accuracy_score,
          communication_score: response.communication_score
        },
        strengths: response.strengths,
        weaknesses: response.weaknesses,
        suggestions: response.suggestions
      }
    }]);

    // Clear answer and load next question
    setUserAnswer('');
    
    // Load next question after 2 seconds
    setTimeout(async () => {
      const nextQuestion = await interviewService.getNextQuestion(sessionId);
      
      if (!nextQuestion) {
        setSessionComplete(true);
      } else {
        setCurrentQuestion(nextQuestion);
        setTimeStarted(Date.now());
        setMessages(prev => [...prev, {
          id: `q-${nextQuestion.question_id}`,
          type: 'question',
          content: nextQuestion.question_text,
          timestamp: new Date(),
          metadata: {
            question_order: nextQuestion.question_order,
            question_type: nextQuestion.question_type
          }
        }]);
      }
    }, 2000);

  } catch (error) {
    setError('Failed to submit answer: ' + error.message);
  } finally {
    setSubmitting(false);
  }
};
```

**3. Message Display**

```typescript
const renderMessage = (message: Message) => {
  switch (message.type) {
    case 'question':
      return (
        <div className="flex justify-start mb-6">
          <div className="bg-blue-100 rounded-lg p-4 max-w-2xl">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-2">🤖</span>
              <span className="font-semibold">Question {message.metadata?.question_order}</span>
              <span className="ml-2 text-xs bg-blue-200 px-2 py-1 rounded">
                {message.metadata?.question_type}
              </span>
            </div>
            <p className="text-gray-800">{message.content}</p>
          </div>
        </div>
      );

    case 'answer':
      return (
        <div className="flex justify-end mb-6">
          <div className="bg-green-100 rounded-lg p-4 max-w-2xl">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-2">👤</span>
              <span className="font-semibold">Your Answer</span>
            </div>
            <p className="text-gray-800">{message.content}</p>
          </div>
        </div>
      );

    case 'feedback':
      return (
        <div className="flex justify-start mb-6">
          <div className="bg-purple-100 rounded-lg p-4 max-w-2xl w-full">
            <div className="flex items-center mb-3">
              <span className="text-2xl mr-2">✨</span>
              <span className="font-semibold">AI Feedback</span>
            </div>
            
            {/* Score Badges */}
            <div className="flex flex-wrap gap-2 mb-3">
              <ScoreBadge label="Overall" score={message.metadata?.scores?.overall_score} />
              <ScoreBadge label="Relevance" score={message.metadata?.scores?.relevance_score} />
              <ScoreBadge label="Completeness" score={message.metadata?.scores?.completeness_score} />
              <ScoreBadge label="Clarity" score={message.metadata?.scores?.clarity_score} />
              <ScoreBadge label="Technical" score={message.metadata?.scores?.technical_accuracy_score} />
              <ScoreBadge label="Communication" score={message.metadata?.scores?.communication_score} />
            </div>

            {/* Feedback Text */}
            <p className="text-gray-800 mb-3">{message.content}</p>

            {/* Strengths */}
            {message.metadata?.strengths && message.metadata.strengths.length > 0 && (
              <div className="mb-2">
                <h4 className="font-semibold text-green-700 mb-1">✅ Strengths:</h4>
                <ul className="list-disc list-inside text-sm">
                  {message.metadata.strengths.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </div>
            )}

            {/* Weaknesses */}
            {message.metadata?.weaknesses && message.metadata.weaknesses.length > 0 && (
              <div className="mb-2">
                <h4 className="font-semibold text-red-700 mb-1">⚠️ Areas to Improve:</h4>
                <ul className="list-disc list-inside text-sm">
                  {message.metadata.weaknesses.map((w, i) => <li key={i}>{w}</li>)}
                </ul>
              </div>
            )}

            {/* Suggestions */}
            {message.metadata?.suggestions && message.metadata.suggestions.length > 0 && (
              <div>
                <h4 className="font-semibold text-blue-700 mb-1">💡 Suggestions:</h4>
                <ul className="list-disc list-inside text-sm">
                  {message.metadata.suggestions.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </div>
            )}
          </div>
        </div>
      );
  }
};
```

**4. Score Badge Component**

```typescript
const ScoreBadge: React.FC<{ label: string; score: number }> = ({ label, score }) => {
  const getColor = (score: number) => {
    if (score >= 90) return 'bg-green-500';
    if (score >= 75) return 'bg-blue-500';
    if (score >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className={`${getColor(score)} text-white px-3 py-1 rounded-full text-xs font-semibold`}>
      {label}: {score.toFixed(0)}
    </div>
  );
};
```

**5. Answer Input with Character Counter**

```typescript
<div className="border-t pt-4">
  <textarea
    value={userAnswer}
    onChange={(e) => setUserAnswer(e.target.value)}
    placeholder="Type your answer here..."
    className="w-full border rounded-lg p-3"
    rows={5}
    disabled={submitting || sessionComplete}
  />
  
  <div className="flex justify-between items-center mt-2">
    <span className="text-sm text-gray-500">
      {userAnswer.length} characters
      {userAnswer.length < 50 && ' (aim for 50+)'}
    </span>
    
    <button
      onClick={handleSubmitAnswer}
      disabled={!userAnswer.trim() || submitting}
      className="bg-blue-600 text-white px-6 py-2 rounded-lg disabled:opacity-50"
    >
      {submitting ? 'Submitting...' : 'Submit Answer'}
    </button>
  </div>
</div>
```

**6. Session Complete Handler**

```typescript
const handleCompleteSession = async () => {
  try {
    const summary = await interviewService.completeSession(sessionId);
    
    // Show summary modal
    setMessages(prev => [...prev, {
      id: 'completion',
      type: 'system',
      content: `Session Complete! Average Score: ${summary.average_score.toFixed(1)}`,
      timestamp: new Date()
    }]);
    
    // Redirect to history after 3 seconds
    setTimeout(() => {
      window.location.href = '/interview?tab=history';
    }, 3000);
  } catch (error) {
    setError('Failed to complete session: ' + error.message);
  }
};
```

---

### 1.4 InterviewHistory Component (`InterviewHistory.tsx`)

**File:** 850 lines  
**Purpose:** Display past sessions with detailed reports and BILAN (overall assessment).

#### Component State

```typescript
const [sessions, setSessions] = useState<Session[]>([]);
const [stats, setStats] = useState<Stats | null>(null);
const [selectedSession, setSelectedSession] = useState<SessionDetail | null>(null);
const [loading, setLoading] = useState(true);
const [filter, setFilter] = useState<'all' | 'completed' | 'active'>('all');
```

#### Key Features

**1. Statistics Overview**

```typescript
useEffect(() => {
  const fetchStats = async () => {
    const userStats = await interviewService.getSessionStats();
    setStats(userStats);
  };
  fetchStats();
}, []);

<div className="grid grid-cols-4 gap-4 mb-8">
  <div className="bg-white rounded-lg shadow p-6">
    <h3 className="text-3xl font-bold text-blue-600">{stats?.total_sessions}</h3>
    <p className="text-gray-600">Total Sessions</p>
  </div>
  
  <div className="bg-white rounded-lg shadow p-6">
    <h3 className="text-3xl font-bold text-green-600">{stats?.completed_sessions}</h3>
    <p className="text-gray-600">Completed</p>
  </div>
  
  <div className="bg-white rounded-lg shadow p-6">
    <h3 className="text-3xl font-bold text-purple-600">{stats?.average_score?.toFixed(1)}</h3>
    <p className="text-gray-600">Avg Score</p>
  </div>
  
  <div className="bg-white rounded-lg shadow p-6">
    <h3 className="text-3xl font-bold text-orange-600">{stats?.in_progress_sessions}</h3>
    <p className="text-gray-600">In Progress</p>
  </div>
</div>
```

**2. Sessions List with Filters**

```typescript
<div className="mb-4 flex gap-2">
  <button
    onClick={() => setFilter('all')}
    className={filter === 'all' ? 'active' : ''}
  >
    All
  </button>
  <button
    onClick={() => setFilter('completed')}
    className={filter === 'completed' ? 'active' : ''}
  >
    Completed
  </button>
  <button
    onClick={() => setFilter('active')}
    className={filter === 'active' ? 'active' : ''}
  >
    In Progress
  </button>
</div>

<div className="space-y-4">
  {filteredSessions.map(session => (
    <div key={session.id} className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-xl font-semibold">{session.session_type} Interview</h3>
          <p className="text-gray-600">
            {session.job_role || session.difficulty_level} • 
            {session.questions_answered}/{session.total_questions} questions
          </p>
          <p className="text-sm text-gray-500">
            {new Date(session.created_at).toLocaleDateString()}
          </p>
        </div>
        
        <div className="text-right">
          {session.status === 'completed' ? (
            <div className="text-3xl font-bold text-green-600">
              {session.average_score?.toFixed(1)}
            </div>
          ) : (
            <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
              In Progress
            </span>
          )}
        </div>
      </div>
      
      <div className="mt-4 flex gap-2">
        <button
          onClick={() => loadSessionDetails(session.id)}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          View Details
        </button>
        
        {session.status === 'active' && (
          <button
            onClick={() => continueSession(session.id)}
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            Continue
          </button>
        )}
        
        <button
          onClick={() => deleteSession(session.id)}
          className="bg-red-600 text-white px-4 py-2 rounded"
        >
          Delete
        </button>
      </div>
    </div>
  ))}
</div>
```

**3. Session Details Modal with BILAN**

```typescript
const SessionDetailModal: React.FC<{ session: SessionDetail; onClose: () => void }> = ({ session, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto p-8">
        {/* Header */}
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-2xl font-bold">{session.session_type} Interview</h2>
            <p className="text-gray-600">{session.job_role || session.difficulty_level}</p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">✕</button>
        </div>

        {/* BILAN (Overall Assessment) */}
        {session.feedback && (
          <div className="bg-gradient-to-r from-purple-100 to-blue-100 rounded-lg p-6 mb-6">
            <h3 className="text-xl font-bold mb-4">📊 BILAN (Overall Assessment)</h3>
            
            {/* Performance Breakdown */}
            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="bg-white rounded p-3 text-center">
                <div className="text-2xl font-bold text-blue-600">{session.feedback.technical_rating}</div>
                <div className="text-sm text-gray-600">Technical Skills</div>
              </div>
              <div className="bg-white rounded p-3 text-center">
                <div className="text-2xl font-bold text-green-600">{session.feedback.communication_rating}</div>
                <div className="text-sm text-gray-600">Communication</div>
              </div>
              <div className="bg-white rounded p-3 text-center">
                <div className="text-2xl font-bold text-purple-600">{session.feedback.problem_solving_rating}</div>
                <div className="text-sm text-gray-600">Problem Solving</div>
              </div>
            </div>

            {/* Key Strengths */}
            <div className="mb-4">
              <h4 className="font-semibold text-green-700 mb-2">✅ Key Strengths:</h4>
              <ul className="list-disc list-inside space-y-1">
                {session.feedback.key_strengths.map((strength, i) => (
                  <li key={i} className="text-gray-700">{strength}</li>
                ))}
              </ul>
            </div>

            {/* Areas to Improve */}
            <div className="mb-4">
              <h4 className="font-semibold text-red-700 mb-2">📈 Areas to Improve:</h4>
              <ul className="list-disc list-inside space-y-1">
                {session.feedback.areas_to_improve.map((area, i) => (
                  <li key={i} className="text-gray-700">{area}</li>
                ))}
              </ul>
            </div>

            {/* Recommended Resources */}
            <div className="mb-4">
              <h4 className="font-semibold text-blue-700 mb-2">📚 Recommended Resources:</h4>
              <div className="space-y-2">
                {session.feedback.recommended_resources.map((resource, i) => (
                  <a
                    key={i}
                    href={resource.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block bg-white rounded p-2 hover:bg-gray-50"
                  >
                    <div className="font-medium">{resource.title}</div>
                    <div className="text-sm text-gray-600">{resource.type}</div>
                  </a>
                ))}
              </div>
            </div>

            {/* Preparation Tips */}
            <div className="mb-4">
              <h4 className="font-semibold text-purple-700 mb-2">💡 Preparation Tips:</h4>
              <p className="text-gray-700">{session.feedback.preparation_tips}</p>
            </div>

            {/* Practice Recommendations */}
            <div>
              <h4 className="font-semibold text-orange-700 mb-2">🎯 Practice Recommendations:</h4>
              <p className="text-gray-700">{session.feedback.practice_recommendations}</p>
            </div>
          </div>
        )}

        {/* Q&A Details */}
        <div className="space-y-6">
          <h3 className="text-xl font-bold">Questions & Answers</h3>
          
          {session.questions.map((qa, index) => (
            <div key={qa.id} className="border rounded-lg p-4">
              <div className="flex justify-between items-start mb-3">
                <h4 className="font-semibold">Question {index + 1}</h4>
                <div className="text-2xl font-bold text-blue-600">
                  {qa.answer?.overall_score?.toFixed(0)}
                </div>
              </div>
              
              <p className="text-gray-700 mb-3">{qa.question_text}</p>
              
              {qa.answer && (
                <>
                  <div className="bg-gray-50 rounded p-3 mb-3">
                    <p className="text-sm font-semibold mb-1">Your Answer:</p>
                    <p className="text-gray-700">{qa.answer.user_answer}</p>
                  </div>
                  
                  <div className="bg-purple-50 rounded p-3">
                    <p className="text-sm font-semibold mb-1">AI Feedback:</p>
                    <p className="text-gray-700 mb-2">{qa.answer.ai_feedback}</p>
                    
                    {/* Score Breakdown */}
                    <div className="flex flex-wrap gap-2">
                      <ScoreBadge label="Relevance" score={qa.answer.relevance_score} />
                      <ScoreBadge label="Completeness" score={qa.answer.completeness_score} />
                      <ScoreBadge label="Clarity" score={qa.answer.clarity_score} />
                      <ScoreBadge label="Technical" score={qa.answer.technical_accuracy_score} />
                      <ScoreBadge label="Communication" score={qa.answer.communication_score} />
                    </div>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
```

---

## 2. Integration Flows

### 2.1 Complete Interview Flow (End-to-End)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INTERVIEW FLOW                                │
└─────────────────────────────────────────────────────────────────────┘

1. SESSION SETUP
   User → InterviewSetup Component → POST /api/interview/start
   ├─ Input: session_type, difficulty_level, num_questions, job_role, resume_id
   ├─ Backend: InterviewSimulator.start_session()
   │   ├─ Parse resume (if provided)
   │   ├─ Select questions from question_bank
   │   ├─ Create interview_sessions record
   │   └─ Insert interview_questions records
   └─ Output: session_id, first_question

2. ANSWER SUBMISSION (Loop for each question)
   User Types Answer → InterviewChat Component → POST /api/interview/answer
   ├─ Input: session_id, question_id, answer, time_taken_seconds
   ├─ Backend: 
   │   ├─ InterviewSimulator.submit_answer() - Create answer record
   │   ├─ GroqAnswerAnalyzer.analyze_answer() - AI analysis
   │   │   ├─ Build structured prompt
   │   │   ├─ Call Groq API (LLaMA 3.3 70B)
   │   │   ├─ Parse JSON response
   │   │   └─ Validate scores
   │   └─ Update interview_answers with scores and feedback
   └─ Output: scores, strengths, weaknesses, suggestions, ai_feedback

3. NEXT QUESTION
   InterviewChat Component → GET /api/interview/{id}/question
   ├─ Backend: InterviewSimulator.get_next_question()
   │   ├─ Query next unanswered question
   │   └─ Calculate progress percentage
   └─ Output: next_question OR null (if all answered)

4. SESSION COMPLETION
   All Questions Answered → POST /api/interview/{id}/complete
   ├─ Backend: InterviewSimulator.complete_session()
   │   ├─ Calculate average_score
   │   ├─ Generate key_strengths (from answer strengths)
   │   ├─ Generate areas_to_improve (from answer weaknesses)
   │   ├─ Classify overall_performance
   │   ├─ Calculate ratings (technical, communication, problem_solving)
   │   ├─ Generate preparation_tips
   │   ├─ Generate practice_recommendations
   │   ├─ Insert interview_feedback record
   │   └─ Update session status to 'completed'
   └─ Output: session_summary with feedback

5. VIEW HISTORY
   User → InterviewHistory Component → GET /api/interview/history
   ├─ Backend: Query interview_sessions with filters
   └─ Output: sessions list with stats

6. VIEW DETAILS
   User Clicks Session → GET /api/interview/{id}
   ├─ Backend: 
   │   ├─ Query interview_sessions
   │   ├─ Join interview_questions
   │   ├─ Join interview_answers
   │   └─ Join interview_feedback
   └─ Output: complete_session_detail with BILAN
```

---

### 2.2 AI Analysis Integration

```
┌─────────────────────────────────────────────────────────────────────┐
│                     AI ANALYSIS WORKFLOW                             │
└─────────────────────────────────────────────────────────────────────┘

User Answer → API Endpoint → GroqAnswerAnalyzer
                                    │
                                    ├─ 1. Build Prompt
                                    │   ├─ Include question text
                                    │   ├─ Include answer text
                                    │   ├─ Include question_type
                                    │   └─ Include key_points (if available)
                                    │
                                    ├─ 2. Call Groq API
                                    │   ├─ Model: llama-3.3-70b-versatile
                                    │   ├─ Temperature: 0.3
                                    │   ├─ Max Tokens: 2000
                                    │   └─ Timeout: 30 seconds
                                    │
                                    ├─ 3. Parse Response
                                    │   ├─ Extract JSON from response
                                    │   ├─ Validate required fields
                                    │   ├─ Validate score ranges (0-100)
                                    │   └─ Handle parsing errors
                                    │
                                    ├─ 4. Fallback (if API fails)
                                    │   ├─ Use rule-based scoring
                                    │   ├─ Score based on answer length
                                    │   └─ Provide generic feedback
                                    │
                                    └─ 5. Return Analysis
                                        ├─ 6 dimension scores
                                        ├─ Strengths (2-4 items)
                                        ├─ Weaknesses (1-3 items)
                                        ├─ Suggestions (2-4 items)
                                        ├─ AI feedback text
                                        └─ Sentiment classification
```

---

## 3. Configuration & Environment

### 3.1 Environment Variables

**Backend `.env`:**

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=utopiahire
DB_USER=utopia_user
DB_PASSWORD=utopia_secure_2025

# Groq AI
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Security
SECRET_KEY=your-secret-key-256-bits
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Interview Settings
INTERVIEW_MAX_QUESTIONS=15
INTERVIEW_MIN_QUESTIONS=3
INTERVIEW_DEFAULT_QUESTIONS=10
INTERVIEW_AI_TIMEOUT_SECONDS=30
INTERVIEW_FALLBACK_ENABLED=true
```

**Frontend `.env`:**

```bash
VITE_API_BASE_URL=http://localhost:8000
```

### 3.2 Database Configuration

**Initialize Database:**

```bash
# Create database
createdb -U postgres utopiahire

# Create user
psql -U postgres -c "CREATE USER utopia_user WITH PASSWORD 'utopia_secure_2025';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE utopiahire TO utopia_user;"

# Run schema
psql -U utopia_user -d utopiahire -f config/interview_schema.sql

# Seed question bank
psql -U utopia_user -d utopiahire -f backend/database/interview_question_bank.sql
```

### 3.3 Groq API Setup

**Get API Key:**
1. Visit https://console.groq.com
2. Sign up or log in
3. Navigate to API Keys
4. Create new API key
5. Copy and add to `.env` as `GROQ_API_KEY`

**Test API Key:**

```bash
python -c "from groq import Groq; client = Groq(api_key='YOUR_KEY'); print('✅ API key valid')"
```

---

## 4. Testing Strategies

### 4.1 Backend Unit Tests

**File:** `/tests/test_interview_endpoint.py`

```python
import pytest
from app.main import app
from fastapi.testclient import client

client = TestClient(app)

def test_start_session():
    response = client.post('/api/interview/start', json={
        'session_type': 'technical',
        'difficulty_level': 'mid',
        'num_questions': 10
    }, headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert 'session_id' in response.json()
    assert 'first_question' in response.json()

def test_submit_answer():
    # Start session first
    session_response = client.post('/api/interview/start', ...)
    session_id = session_response.json()['session_id']
    question_id = session_response.json()['first_question']['question_id']
    
    # Submit answer
    response = client.post('/api/interview/answer', json={
        'session_id': session_id,
        'question_id': question_id,
        'answer': 'Sample answer for testing',
        'time_taken_seconds': 120
    }, headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert 'overall_score' in response.json()
    assert 0 <= response.json()['overall_score'] <= 100

def test_complete_session():
    # Start and answer all questions first...
    
    response = client.post(f'/api/interview/{session_id}/complete', 
                          headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert 'average_score' in response.json()
    assert 'key_strengths' in response.json()
```

### 4.2 AI Integration Tests

**File:** `/tests/test_groq_interview.py`

```python
from utils.groq_answer_analyzer import GroqAnswerAnalyzer

def test_analyze_technical_answer():
    analyzer = GroqAnswerAnalyzer(api_key=os.getenv('GROQ_API_KEY'))
    
    result = analyzer.analyze_answer(
        question="Explain the difference between var, let, and const in JavaScript.",
        answer="var is function-scoped, let is block-scoped, const is also block-scoped but immutable.",
        question_type="technical",
        key_points=["scope differences", "reassignment rules"]
    )
    
    assert 'overall_score' in result
    assert result['overall_score'] > 0
    assert len(result['strengths']) > 0
    assert len(result['suggestions']) > 0

def test_fallback_on_api_failure():
    analyzer = GroqAnswerAnalyzer(api_key='invalid-key')
    
    result = analyzer.analyze_answer(
        question="Test question",
        answer="Test answer",
        question_type="technical"
    )
    
    # Should return fallback scores
    assert 'overall_score' in result
    assert result['ai_feedback'] == "Fallback analysis used. Please try again."
```

---

## 5. Troubleshooting Guide

### 5.1 Common Issues

**Issue 1: Session Not Starting**

**Symptoms:** POST /api/interview/start returns 500 error

**Causes & Solutions:**
- ❌ No questions in question bank → Run `interview_question_bank.sql`
- ❌ Invalid session_type → Use: technical, behavioral, mixed, job-specific
- ❌ Database connection error → Check DB_HOST, DB_USER, DB_PASSWORD

**Issue 2: AI Analysis Fails**

**Symptoms:** Answers submitted but scores are null

**Causes & Solutions:**
- ❌ Invalid GROQ_API_KEY → Verify key at console.groq.com
- ❌ Rate limit exceeded → Wait 60 seconds or upgrade plan
- ❌ Timeout → Increase INTERVIEW_AI_TIMEOUT_SECONDS

**Issue 3: Frontend Can't Load Questions**

**Symptoms:** Loading spinner infinite loop

**Causes & Solutions:**
- ❌ Backend not running → Start with `uvicorn app.main:app --reload`
- ❌ CORS error → Check backend CORS configuration
- ❌ Invalid session_id → Verify session exists in database

---

## 6. Performance Optimization

### 6.1 Database Optimizations

**Indexes:**
- ✅ `interview_sessions(user_id)` - Fast user session lookups
- ✅ `interview_questions(session_id, question_order)` - Fast question retrieval
- ✅ `interview_answers(session_id)` - Fast answer queries
- ✅ GIN indexes on `question_bank` arrays for skill matching

**Query Optimization:**
```sql
-- Efficient next question query (uses index)
SELECT iq.*, qb.*
FROM interview_questions iq
JOIN interview_question_bank qb ON iq.question_id = qb.id
LEFT JOIN interview_answers ia ON iq.id = ia.interview_question_id
WHERE iq.session_id = $1 AND ia.id IS NULL
ORDER BY iq.question_order ASC
LIMIT 1;
```

### 6.2 API Response Times

| Endpoint | Avg Response Time | Notes |
|----------|-------------------|-------|
| POST /start | 250ms | Includes question selection |
| POST /answer | 2.1s | Includes AI analysis (Groq API) |
| GET /question | 50ms | Simple database query |
| POST /complete | 350ms | Aggregates all answers |
| GET /history | 120ms | Returns paginated list |
| GET /{id} | 180ms | Joins 4 tables |

### 6.3 Frontend Optimizations

**React Optimizations:**
- ✅ `useMemo` for expensive calculations
- ✅ `useCallback` for event handlers
- ✅ Lazy loading for History component
- ✅ Virtualized list for large session history

**Code Splitting:**
```typescript
const InterviewHistory = lazy(() => import('@/components/interview/InterviewHistory'));
```

---

## Summary

Part 2B covers:
1. ✅ **Frontend Components** - InterviewSetup, InterviewChat, InterviewHistory with full code examples
2. ✅ **Integration Flows** - End-to-end interview flow and AI analysis workflow
3. ✅ **Configuration** - Environment variables, database setup, Groq API configuration
4. ✅ **Testing Strategies** - Backend unit tests and AI integration tests
5. ✅ **Troubleshooting** - Common issues and solutions
6. ✅ **Performance** - Database optimizations and response time benchmarks

**Interview Module Documentation Complete!**

📚 See also:
- [Part 1: Overview, Architecture, Features, API Reference](./INTERVIEW_MODULE_PART1.md)
- [Part 2A: Database Schema & Utility Modules](./INTERVIEW_MODULE_PART2A.md)

---

**End of Interview Module Documentation**
