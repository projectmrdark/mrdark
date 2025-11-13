'use client';

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const sendMessage = async () => {
    if (!message.trim()) return;

    // Add user message to chat
    const userMessage = { role: 'user', content: message };
    setMessages((prev) => [...prev, userMessage]);
    setMessage('');
    setLoading(true);

    try {
      // Call backend API
      const response = await axios.post(`${API_URL}/api/chat/simple`, {
        message: message,
      });

      // Add AI response to chat
      const aiMessage = {
        role: 'assistant',
        content: response.data.response,
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'error',
        content: 'Failed to get response from AI. Please try again.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Mr.Dark AI Agent Platform
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Powered by VanChin AI
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Chat Messages */}
        <div className="bg-gray-900/30 rounded-lg border border-gray-800 p-6 mb-4 min-h-[500px] max-h-[600px] overflow-y-auto">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              <div className="text-center">
                <div className="text-6xl mb-4">💬</div>
                <p className="text-lg">Start a conversation with Mr.Dark AI</p>
                <p className="text-sm mt-2">Ask me anything!</p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${
                    msg.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-3 ${
                      msg.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : msg.role === 'error'
                        ? 'bg-red-900/50 text-red-200 border border-red-700'
                        : 'bg-gray-800 text-gray-100'
                    }`}
                  >
                    <div className="text-xs font-semibold mb-1 opacity-70">
                      {msg.role === 'user' ? 'You' : msg.role === 'error' ? 'Error' : 'AI'}
                    </div>
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-gray-800 text-gray-100 rounded-lg px-4 py-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="bg-gray-900/30 rounded-lg border border-gray-800 p-4">
          <div className="flex space-x-4">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message... (Press Enter to send)"
              className="flex-1 bg-gray-800 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={3}
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              disabled={loading || !message.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              {loading ? 'Sending...' : 'Send'}
            </button>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            Press Enter to send, Shift+Enter for new line
          </div>
        </div>

        {/* Info Section */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-900/30 rounded-lg border border-gray-800 p-4">
            <div className="text-sm font-semibold text-blue-400 mb-2">🚀 Features</div>
            <ul className="text-xs text-gray-400 space-y-1">
              <li>• AI-powered chat</li>
              <li>• Code execution</li>
              <li>• Multi-model support</li>
            </ul>
          </div>
          <div className="bg-gray-900/30 rounded-lg border border-gray-800 p-4">
            <div className="text-sm font-semibold text-purple-400 mb-2">⚡ Status</div>
            <ul className="text-xs text-gray-400 space-y-1">
              <li>• Backend: Connected</li>
              <li>• AI: VanChin API</li>
              <li>• Version: 1.0.0</li>
            </ul>
          </div>
          <div className="bg-gray-900/30 rounded-lg border border-gray-800 p-4">
            <div className="text-sm font-semibold text-green-400 mb-2">📊 Models</div>
            <ul className="text-xs text-gray-400 space-y-1">
              <li>• 10+ AI endpoints</li>
              <li>• Auto rotation</li>
              <li>• High availability</li>
            </ul>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 mt-12">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-gray-500">
          <p>Mr.Dark AI Agent Platform © 2024 - Built with Next.js, FastAPI, and VanChin AI</p>
        </div>
      </footer>
    </div>
  );
}
