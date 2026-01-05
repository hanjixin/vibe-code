import React, { useState, useEffect } from 'react';
import { FileTree } from './FileTree';
import { CodeEditor } from './CodeEditor';
import { Save, RefreshCw } from 'lucide-react';

interface WorkspacePanelProps {
  className?: string;
}

export const WorkspacePanel: React.FC<WorkspacePanelProps> = ({ className }) => {
  const [fileTree, setFileTree] = useState<any[]>([]);
  const [selectedFile, setSelectedFile] = useState<any>(null);
  const [fileContent, setFileContent] = useState('');
  const [isDirty, setIsDirty] = useState(false);

  const fetchFileTree = async () => {
    try {
      const res = await fetch('/api/files/tree');
      const data = await res.json();
      setFileTree(data);
    } catch (err) {
      console.error("Failed to fetch file tree", err);
    }
  };

  useEffect(() => {
    fetchFileTree();
  }, []);

  const handleFileSelect = async (file: any) => {
    if (isDirty) {
      if (!confirm("You have unsaved changes. Discard them?")) return;
    }
    
    setSelectedFile(file);
    try {
      const res = await fetch(`/api/files/content?path=${encodeURIComponent(file.path)}`);
      const data = await res.json();
      setFileContent(data.content);
      setIsDirty(false);
    } catch (err) {
      console.error("Failed to fetch file content", err);
    }
  };

  const handleSave = async () => {
    if (!selectedFile) return;
    
    try {
      await fetch('/api/files/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: selectedFile.path, content: fileContent })
      });
      setIsDirty(false);
      alert("File saved!");
    } catch (err) {
      console.error("Failed to save file", err);
      alert("Failed to save file");
    }
  };

  const getLanguage = (filename: string) => {
    if (filename.endsWith('.py')) return 'python';
    if (filename.endsWith('.ts') || filename.endsWith('.tsx')) return 'typescript';
    if (filename.endsWith('.js') || filename.endsWith('.jsx')) return 'javascript';
    if (filename.endsWith('.html')) return 'html';
    if (filename.endsWith('.css')) return 'css';
    if (filename.endsWith('.json')) return 'json';
    return 'plaintext';
  };

  return (
    <div className={`flex flex-col h-full bg-gray-900 border-l border-gray-700 ${className}`}>
      <div className="flex items-center justify-between p-2 bg-gray-800 border-b border-gray-700">
        <span className="text-sm font-semibold text-gray-300">Workspace</span>
        <div className="flex gap-2">
          <button onClick={fetchFileTree} className="p-1 hover:bg-gray-700 rounded text-gray-400" title="Refresh">
            <RefreshCw size={16} />
          </button>
          <button 
            onClick={handleSave} 
            className={`p-1 rounded ${isDirty ? 'text-blue-400 hover:bg-gray-700' : 'text-gray-600'}`}
            disabled={!isDirty}
            title="Save"
          >
            <Save size={16} />
          </button>
        </div>
      </div>
      
      <div className="flex-1 flex overflow-hidden">
        <div className="w-1/3 border-r border-gray-700 overflow-y-auto bg-gray-900">
          <FileTree data={fileTree} onSelect={handleFileSelect} />
        </div>
        <div className="flex-1 bg-[#1e1e1e]">
          {selectedFile ? (
            <CodeEditor 
              code={fileContent} 
              language={getLanguage(selectedFile.name)}
              onChange={(val) => {
                setFileContent(val || '');
                setIsDirty(true);
              }}
            />
          ) : (
            <div className="flex items-center justify-center h-full text-gray-500 text-sm">
              Select a file to edit
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
