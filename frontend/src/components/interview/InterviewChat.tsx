import { useState, useEffect, useRef } from 'react';
import { interviewService, Question, AnswerFeedback } from '../../services/interview.service.ts';

interface Message {
  id: string;
  role: 'interviewer' | 'user';
  content: string;
  timestamp: Date;
  feedback?: AnswerFeedback;
  scores?: any;
}

interface InterviewChatProps {
  sessionId: number | null;
  onSessionComplete: () => void;
}

const InterviewChat = ({ sessionId, onSessionComplete }: InterviewChatProps) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [loadingQuestion, setLoadingQuestion] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionInfo, setSessionInfo] = useState<any>(null);
  const [startTime, setStartTime] = useState<Date | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const sessionLoadedRef = useRef<number | null>(null);

  useEffect(() => {
    if (sessionId && sessionId !== sessionLoadedRef.current) {
      sessionLoadedRef.current = sessionId;
      loadSession();
    }
  }, [sessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadSession = async () => {
    if (!sessionId || loading) {
      if (!sessionId) {
        setError('No active session. Please start a new interview.');
      }
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // Load session details
      const session = await interviewService.getSessionDetails(sessionId);
      setSessionInfo(session);

      // If session is completed, redirect
      if (session.status === 'completed') {
        onSessionComplete();
        return;
      }

      // Add welcome message
      const welcomeMsg: Message = {
        id: 'welcome',
        role: 'interviewer',
        content: `Hello! I'm your AI interviewer today. We'll be conducting a ${session.session_type} interview for the ${session.job_role} position at ${session.difficulty_level} level. I have ${session.total_questions} questions prepared for you.\n\nLet's begin! Take your time with each answer and be as detailed as possible.`,
        timestamp: new Date()
      };
      
      const newMessages: Message[] = [welcomeMsg];

      // Load first question if no questions answered yet
      if (session.questions_answered === 0) {
        setMessages(newMessages);
        await loadNextQuestion();
      } else {
        // Reload previous Q&A
        session.questions_and_answers.forEach((qa: any) => {
          const qMsg: Message = {
            id: `q-${qa.question_number}`,
            role: 'interviewer',
            content: `**Question ${qa.question_number}/${session.total_questions}:**\n\n${qa.question_text}`,
            timestamp: new Date()
          };
          
          const aMsg: Message = {
            id: `a-${qa.question_number}`,
            role: 'user',
            content: qa.user_answer,
            timestamp: new Date(),
            feedback: qa.feedback,
            scores: qa.scores
          };

          newMessages.push(qMsg, aMsg);
        });
        
        setMessages(newMessages);

        // Load next question if not completed
        if (session.questions_answered < session.total_questions) {
          await loadNextQuestion();
        }
      }
    } catch (err: any) {
      console.error('Error loading session:', err);
      setError(err.response?.data?.detail || 'Failed to load interview session');
    } finally {
      setLoading(false);
    }
  };

  const loadNextQuestion = async () => {
    if (!sessionId || loadingQuestion) return;

    try {
      setLoadingQuestion(true);
      const response = await interviewService.getNextQuestion(sessionId);
      setCurrentQuestion(response);
      setStartTime(new Date());

      const questionMsg: Message = {
        id: `q-${response.question_number}`,
        role: 'interviewer',
        content: `**Question ${response.question_number}/${response.total_questions}** (${response.question_type}):\n\n${response.question_text}`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, questionMsg]);
    } catch (err: any) {
      console.error('Error loading question:', err);
      setError(err.response?.data?.detail || 'Failed to load next question');
    } finally {
      setLoadingQuestion(false);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!answer.trim() || !sessionId || !currentQuestion) return;
    
    // Validate minimum answer length
    if (answer.trim().length < 10) {
      setError('Answer must be at least 10 characters long');
      return;
    }
    
    // Prevent duplicate submissions
    if (submitting) return;

    try {
      setSubmitting(true);
      setError(null);

      // Calculate time taken
      const timeTaken = startTime ? Math.floor((new Date().getTime() - startTime.getTime()) / 1000) : 0;

      // Add user's answer to messages
      const answerMsg: Message = {
        id: `a-${currentQuestion.question_number}`,
        role: 'user',
        content: answer,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, answerMsg]);

      // Submit answer with question_id and time_taken_seconds
      const response = await interviewService.submitAnswer({
        session_id: sessionId,
        question_id: currentQuestion.question_id,
        answer: answer,
        time_taken_seconds: timeTaken
      });

      // Add feedback message
      const feedbackMsg: Message = {
        id: `f-${currentQuestion.question_number}`,
        role: 'interviewer',
        content: generateFeedbackMessage(response.feedback, response.scores),
        timestamp: new Date(),
        feedback: response.feedback,
        scores: response.scores
      };
      setMessages(prev => [...prev, feedbackMsg]);

      // Clear answer and current question to prevent resubmission
      setAnswer('');
      setCurrentQuestion(null);
      setStartTime(null);

      // Refetch session info to update the counter
      try {
        const updatedSession = await interviewService.getSessionDetails(sessionId);
        setSessionInfo(updatedSession);
      } catch (err) {
        console.warn('Failed to update session info:', err);
      }

      // Check if there are more questions
      if (response.has_more_questions) {
        // Add transition message
        setTimeout(() => {
          const transitionMsg: Message = {
            id: `t-${currentQuestion.question_number}`,
            role: 'interviewer',
            content: "Great! Let's move on to the next question.",
            timestamp: new Date()
          };
          setMessages(prev => [...prev, transitionMsg]);
          
          // Load next question
          setTimeout(() => {
            loadNextQuestion();
          }, 1000);
        }, 2000);
      } else {
        // Interview complete
        setTimeout(() => {
          handleCompleteInterview();
        }, 2000);
      }
    } catch (err: any) {
      console.error('Error submitting answer:', err);
      const errorDetail = err.response?.data?.detail || err.message || 'Failed to submit answer';
      setError(`Submit failed: ${errorDetail}`);
      
      // Remove the user's answer message if submission failed
      setMessages(prev => prev.filter(msg => msg.id !== `a-${currentQuestion?.question_number}`));
    } finally {
      setSubmitting(false);
    }
  };

  const handleCompleteInterview = async () => {
    if (!sessionId) return;

    try {
      const completionMsg: Message = {
        id: 'completion',
        role: 'interviewer',
        content: "🎉 Congratulations! You've completed the interview. Let me generate your final report...",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, completionMsg]);

      const completionResponse = await interviewService.completeSession(sessionId);
      
      // Show completion results
      const resultsMsg: Message = {
        id: 'completion-results',
        role: 'interviewer',
        content: `## 🎊 Interview Completed!\n\n${completionResponse.message}\n\n**Average Score: ${completionResponse.average_scores.overall.toFixed(1)}/100**\n\n**Performance Rating: ${completionResponse.performance}**\n\n📊 **Detailed Scores:**\n- Relevance: ${completionResponse.average_scores.relevance.toFixed(1)}/100\n- Completeness: ${completionResponse.average_scores.completeness.toFixed(1)}/100\n- Clarity: ${completionResponse.average_scores.clarity.toFixed(1)}/100\n- Technical Accuracy: ${completionResponse.average_scores.technical_accuracy.toFixed(1)}/100\n- Communication: ${completionResponse.average_scores.communication.toFixed(1)}/100\n\n✅ **Key Strengths:**\n${completionResponse.feedback.strengths.map((s: string) => `- ${s}`).join('\n')}\n\n⚠️ **Areas to Improve:**\n${completionResponse.feedback.areas_to_improve.map((a: string) => `- ${a}`).join('\n')}\n\n💡 **Recommendations:**\n${completionResponse.feedback.recommended_resources.map((r: string) => `- ${r}`).join('\n')}\n\nYou can view your full interview history by clicking on the "Interview History" tab.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, resultsMsg]);
      
      // Delay navigation to allow user to read results
      setTimeout(() => {
        onSessionComplete();
      }, 5000);
    } catch (err: any) {
      console.error('Error completing interview:', err);
      setError(err.response?.data?.detail || 'Failed to complete interview');
    }
  };

  const generateFeedbackMessage = (feedback: AnswerFeedback, scores: any): string => {
    let message = `**Feedback on your answer:**\n\n`;
    message += `📊 **Scores:**\n`;
    message += `- Overall: ${scores.overall}/100\n`;
    message += `- Relevance: ${scores.relevance}/100\n`;
    message += `- Completeness: ${scores.completeness}/100\n`;
    message += `- Clarity: ${scores.clarity}/100\n`;
    message += `- Technical Accuracy: ${scores.technical_accuracy}/100\n\n`;
    
    if (feedback.strengths.length > 0) {
      message += `✅ **Strengths:**\n`;
      feedback.strengths.forEach((s: string) => message += `- ${s}\n`);
      message += `\n`;
    }
    
    if (feedback.weaknesses.length > 0) {
      message += `⚠️ **Areas to Improve:**\n`;
      feedback.weaknesses.forEach((w: string) => message += `- ${w}\n`);
      message += `\n`;
    }
    
    if (feedback.missing_points.length > 0) {
      message += `📝 **Key Points Missed:**\n`;
      feedback.missing_points.forEach((m: string) => message += `- ${m}\n`);
      message += `\n`;
    }
    
    if (feedback.suggestions.length > 0) {
      message += `💡 **Suggestions:**\n`;
      feedback.suggestions.forEach((s: string) => message += `- ${s}\n`);
    }
    
    return message;
  };

  const getScoreColor = (score: number): string => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreEmoji = (score: number): string => {
    if (score >= 90) return '🌟';
    if (score >= 80) return '✨';
    if (score >= 70) return '👍';
    if (score >= 60) return '👌';
    return '📝';
  };

  if (!sessionId) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-12 text-center">
        <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M8 12h.01M12 12h.01M16 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No Active Session</h3>
        <p className="text-gray-600">Please start a new interview from the "New Interview" tab.</p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col" style={{ height: 'calc(100vh - 250px)' }}>
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <div>
              <h3 className="font-semibold">AI Interviewer</h3>
              {sessionInfo && (
                <p className="text-sm text-white/80">
                  {sessionInfo.job_role} • {sessionInfo.session_type} • 
                  {currentQuestion 
                    ? ` Question ${currentQuestion.question_number}/${currentQuestion.total_questions}`
                    : ` ${sessionInfo.questions_answered}/${sessionInfo.total_questions} completed`
                  }
                </p>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm">Active</span>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-3xl ${message.role === 'user' ? 'ml-12' : 'mr-12'}`}>
                    <div className={`flex items-start gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}>
                      {/* Avatar */}
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                        message.role === 'user' 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                      }`}>
                        {message.role === 'user' ? (
                          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                        ) : (
                          <span className="text-lg">🤖</span>
                        )}
                      </div>

                      {/* Message Content */}
                      <div className={`flex-1 rounded-lg p-4 ${
                        message.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-white border border-gray-200 text-gray-900'
                      }`}>
                        <div className="whitespace-pre-wrap break-words">
                          {message.content.split('\n').map((line, i) => {
                            // Handle bold text
                            if (line.startsWith('**') && line.endsWith('**')) {
                              return <div key={i} className="font-bold mb-2">{line.replace(/\*\*/g, '')}</div>;
                            }
                            // Handle list items
                            if (line.startsWith('- ')) {
                              return <div key={i} className="ml-4">{line}</div>;
                            }
                            return <div key={i}>{line || <br />}</div>;
                          })}
                        </div>
                        
                        {/* Score badges for feedback */}
                        {message.scores && (
                          <div className="mt-3 flex flex-wrap gap-2">
                            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getScoreColor(message.scores.overall)} bg-white/90`}>
                              {getScoreEmoji(message.scores.overall)} Overall: {message.scores.overall}/100
                            </span>
                          </div>
                        )}

                        <div className={`text-xs mt-2 ${message.role === 'user' ? 'text-blue-100' : 'text-gray-400'}`}>
                          {message.timestamp.toLocaleTimeString()}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              
              {submitting && (
                <div className="flex justify-start">
                  <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    <span className="text-gray-600 text-sm">Analyzing your answer...</span>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border-t border-red-200 p-4">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        )}

        {/* Input Area */}
        {currentQuestion && !loading && (
          <div className="border-t border-gray-200 bg-white p-4">
            <div className="max-w-4xl mx-auto">
              <div className="mb-2 flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">
                  Your Answer:
                </label>
                <div className="flex items-center gap-4">
                  <span className={`text-xs font-medium ${answer.trim().length < 10 ? 'text-red-500' : 'text-green-600'}`}>
                    {answer.trim().length}/10 chars minimum
                  </span>
                  {startTime && (
                    <span className="text-xs text-gray-500">
                      Time: {Math.floor((new Date().getTime() - startTime.getTime()) / 1000)}s
                    </span>
                  )}
                </div>
              </div>
              <div className="flex gap-3">
                <textarea
                  ref={textareaRef}
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && e.ctrlKey && !submitting) {
                      handleSubmitAnswer();
                    }
                  }}
                  placeholder="Type your answer here (min 10 characters)... Press Ctrl+Enter to submit"
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                  rows={4}
                  disabled={submitting}
                />
                <button
                  onClick={handleSubmitAnswer}
                  disabled={!answer.trim() || submitting}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 h-fit"
                >
                  {submitting ? (
                    <>
                      <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Submitting...
                    </>
                  ) : (
                    <>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                      </svg>
                      Submit
                    </>
                  )}
                </button>
              </div>
              <p className="mt-1 text-xs text-gray-500">
                Min 10 characters • Press Ctrl+Enter to submit quickly
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default InterviewChat;
