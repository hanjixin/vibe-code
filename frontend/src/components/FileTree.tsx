import React, { useState } from 'react';
import { ChevronRight, ChevronDown, File, Folder } from 'lucide-react';

interface FileNode {
  name: string;
  path: string;
  type: 'file' | 'directory';
  children?: FileNode[];
}

interface FileTreeProps {
  data: FileNode[];
  onSelect: (file: FileNode) => void;
}

const FileTreeNode: React.FC<{ node: FileNode; onSelect: (file: FileNode) => void; depth: number }> = ({ node, onSelect, depth }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleClick = () => {
    if (node.type === 'directory') {
      setIsOpen(!isOpen);
    } else {
      onSelect(node);
    }
  };

  return (
    <div>
      <div 
        className="flex items-center gap-1 py-1 px-2 hover:bg-gray-700 cursor-pointer text-sm text-gray-300"
        style={{ paddingLeft: `${depth * 12 + 8}px` }}
        onClick={handleClick}
      >
        {node.type === 'directory' && (
          isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />
        )}
        {node.type === 'directory' ? (
          <Folder size={14} className="text-blue-400" />
        ) : (
          <File size={14} className="text-gray-400 ml-4" />
        )}
        <span className="truncate">{node.name}</span>
      </div>
      {isOpen && node.children && (
        <div>
          {node.children.map((child) => (
            <FileTreeNode key={child.path} node={child} onSelect={onSelect} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
};

export const FileTree: React.FC<FileTreeProps> = ({ data, onSelect }) => {
  return (
    <div className="overflow-y-auto h-full">
      {data.map((node) => (
        <FileTreeNode key={node.path} node={node} onSelect={onSelect} depth={0} />
      ))}
    </div>
  );
};
