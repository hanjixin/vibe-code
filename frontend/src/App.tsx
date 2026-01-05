import React, { useState } from 'react';
import { Send, Bot, User, Terminal, Play, CheckCircle, GitBranch, Settings } from 'lucide-react';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('autonomy'); // 'autonomy', 'build', 'plan'

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, mode: mode })
      });
      
      const data = await response.json();
      
      // Process trace to extract agent responses
      const agentResponses = data.trace.map((step: any) => ({
        role: 'assistant',
        agent: step.node,
        content: step.content
      }));
      
      setMessages(prev => [...prev, ...agentResponses]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 p-4 border-r border-gray-700 flex flex-col">
        <h1 className="text-xl font-bold mb-6 flex items-center gap-2">
          <Bot className="text-purple-400" />
          Claude Agent
        </h1>
        
        <div className="space-y-2 mb-8">
          <div className="p-2 bg-purple-600 rounded cursor-pointer hover:bg-purple-700 text-center font-semibold">
            New Chat
          </div>
        </div>

        <div className="text-xs text-gray-400 mb-2 uppercase font-semibold">Work Modes</div>
        <div className="space-y-1">
          <div 
            className={`flex items-center gap-2 p-2 text-sm rounded cursor-pointer ${mode === 'build' ? 'bg-gray-700 text-white' : 'text-gray-400 hover:bg-gray-700'}`}
            onClick={() => setMode('build')}
          >
            <Terminal size={16} /> Build Mode
          </div>
          <div 
            className={`flex items-center gap-2 p-2 text-sm rounded cursor-pointer ${mode === 'plan' ? 'bg-gray-700 text-white' : 'text-gray-400 hover:bg-gray-700'}`}
            onClick={() => setMode('plan')}
          >
            <Play size={16} /> Plan Mode
          </div>
          <div 
            className={`flex items-center gap-2 p-2 text-sm rounded cursor-pointer ${mode === 'autonomy' ? 'bg-gray-700 text-white' : 'text-gray-400 hover:bg-gray-700'}`}
            onClick={() => setMode('autonomy')}
          >
            <CheckCircle size={16} /> Max Autonomy
          </div>
        </div>

        <div className="mt-auto pt-4 border-t border-gray-700">
           <div className="flex items-center gap-2 p-2 text-sm text-gray-400 hover:text-white cursor-pointer">
            <GitBranch size={16} /> Checkpoints
          </div>
          <div className="flex items-center gap-2 p-2 text-sm text-gray-400 hover:text-white cursor-pointer">
            <Settings size={16} /> Settings
          </div>
        </div>
      </div>

      {/* Main Chat */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <Bot size={48} className="mb-4 opacity-50" />
              <p>Select a mode and start a task.</p>
            </div>
          )}
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-3xl p-4 rounded-lg ${
                msg.role === 'user' ? 'bg-purple-600' : 'bg-gray-800 border border-gray-700'
              }`}>
                {msg.agent && (
                  <div className="text-xs text-purple-400 mb-1 font-mono flex items-center gap-1">
                    <Bot size={12} /> {msg.agent}
                  </div>
                )}
                <pre className="whitespace-pre-wrap font-sans text-sm">{msg.content}</pre>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex gap-4">
              <div className="bg-gray-800 p-4 rounded-lg border border-gray-700 animate-pulse flex items-center gap-2">
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce delay-150"></div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-700 bg-gray-800">
          <div className="max-w-4xl mx-auto flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder={`Type a message in ${mode} mode...`}
              className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
            />
            <button 
              onClick={sendMessage}
              disabled={loading}
              className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
