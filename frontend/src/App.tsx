import React, { useState, useRef } from 'react';
import { Send, Bot, User, Terminal, Play, CheckCircle, GitBranch, Settings } from 'lucide-react';
import { WorkspacePanel } from './components/WorkspacePanel';
import { Streamdown } from 'streamdown';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('autonomy'); // 'autonomy', 'build', 'plan'
  const [streaming, setStreaming] = useState(false);

  const parseAgentContent = (content: string) => {
    try {
      const aimessageMatch = content.match(/AIMessage\(content='([^']+)'/s);
      if (aimessageMatch && aimessageMatch[1]) {
        let extractedContent = aimessageMatch[1];
        extractedContent = extractedContent
          .replace(/\\n/g, '\n')
          .replace(/\\'/g, "'")
          .replace(/\\"/g, '"')
          .replace(/\\u([0-9a-fA-F]{4})/g, (match, hex) => String.fromCharCode(parseInt(hex, 16)));
        return extractedContent;
      }
      return content
    } catch (error) {
      console.error('Error parsing agent content:', error);
    }
    return content;
  };

  const sendMessage = () => {
    if (!input.trim()) return;
    
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setStreaming(true);

    const eventSource = new EventSource(
      `/api/chat?message=${encodeURIComponent(input)}&mode=${mode}`
    );

    let buffer: any[] = [];

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'end') {
          // End of stream
          if (buffer.length > 0) {
            setMessages(prev => [...prev, ...buffer]);
            buffer = [];
          }
          setLoading(false);
          setStreaming(false);
          eventSource.close();
        } else if (data.type === 'error') {
          // Error
          setMessages(prev => [...prev, {
            role: 'assistant',
            content: `Error: ${data.message}`
          }]);
          setLoading(false);
          setStreaming(false);
          eventSource.close();
        } else {
          // Regular event
          const agentMsg = {
            role: 'assistant',
            agent: data.node,
            content: data.content
          };
          console.log(agentMsg)
          buffer.push(agentMsg);
          // Update UI immediately for real-time effect
          setMessages(prev => [...prev, agentMsg]);
          buffer = [];
        }
      } catch (error) {
        console.error('Error parsing SSE event:', error);
      }
    };

    eventSource.onerror = () => {
      setLoading(false);
      setStreaming(false);
      eventSource.close();
    };
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 p-4 border-r border-gray-700 flex flex-col shrink-0">
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
      <div className="flex-1 flex flex-col min-w-0">
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
                {msg.role === 'assistant' ? (
                  <Streamdown children={msg.content} />
                ) : (
                  <pre className="whitespace-pre-wrap font-sans text-sm">{msg.content}</pre>
                )}
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
              disabled={streaming}
            />
            <button 
              onClick={sendMessage}
              disabled={loading || streaming || !input.trim()}
              className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>

      {/* Workspace Panel */}
      <div className="w-[40%] h-full shrink-0">
        <WorkspacePanel />
      </div>
    </div>
  );
}

export default App;
