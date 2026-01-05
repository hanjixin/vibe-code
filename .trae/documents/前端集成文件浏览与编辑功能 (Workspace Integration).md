这是一个为前端界面增加文件浏览与编辑功能的实施计划。

### 1. 后端 API 扩展 (Backend API Extension)
- **目标**: 提供文件系统访问能力给前端。
- **文件**: `backend/app/main.py`
- **新增接口**:
  - `GET /api/files/tree`: 递归获取项目目录结构（JSON 格式）。
  - `GET /api/files/content?path=...`: 读取指定文件的内容。
  - `POST /api/files/save`: 保存文件内容（`{path: str, content: str}`）。
- **实现方式**: 直接使用 Python `os` 模块实现，确保路径安全（限制在项目根目录下）。

### 2. 前端组件开发 (Frontend Components)
- **目标**: 构建 IDE 风格的 Workspace 面板。
- **依赖**: 安装 `@monaco-editor/react` 用于代码编辑。
- **组件**:
  - `FileTree.tsx`: 递归展示文件目录，支持展开/折叠和点击选择文件。
  - `CodeEditor.tsx`: 封装 Monaco Editor，支持语法高亮和内容修改。
  - `WorkspacePanel.tsx`: 整合 FileTree 和 CodeEditor，管理当前选中文件的状态。

### 3. 前端布局改造 (Layout Refactoring)
- **目标**: 实现三栏布局 (Sidebar | Chat | Workspace)。
- **文件**: `frontend/src/App.tsx`
- **布局调整**:
  - 左侧：导航栏 (保持不变)。
  - 中间：聊天区域 (宽度自适应)。
  - 右侧：Workspace 面板 (固定宽度或可调整，初始设为 40% 宽度)。
- **交互**:
  - 点击 FileTree 中的文件 -> 右侧 Editor 加载内容。
  - 在 Editor 中修改代码 -> 点击保存 -> 调用后端 API 保存。
  - 聊天中 Agent 修改文件后 -> 需手动或自动刷新 FileTree。

### 4. 执行步骤
1.  修改后端 `main.py` 添加 API。
2.  前端安装 Monaco Editor 依赖。
3.  创建前端组件 (`FileTree`, `CodeEditor`, `WorkspacePanel`)。
4.  更新 `App.tsx` 集成新组件。
