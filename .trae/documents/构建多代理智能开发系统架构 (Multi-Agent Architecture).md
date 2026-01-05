这是一个基于 **Claude Code Agent SDK** (概念验证版) 的多代理系统架构实施计划。我们将构建一个高自治、分角色的智能开发环境。

### 1. 项目初始化与基础设施 (Project Setup)
- **目标**: 搭建前后端分离的 Monorepo 架构。
- **后端**: Python 3.12, FastAPI (API层), LangChain/LangGraph (核心逻辑).
- **前端**: React + Vite, TailwindCSS (UI层).
- **环境**: 配置 Poetry 依赖管理与 Docker 沙箱环境基础。

### 2. 核心架构与状态管理 (Core Architecture)
- **LangGraph State**: 定义全局状态 `AgentState`，包含：
  - `messages`: 聊天记录
  - `plan`: 当前任务规划
  - `code_context`: 文件快照与Diff
  - `verification_results`: 测试报告
  - `mode`: 当前工作模式 (Build/Plan/Fast/Autonomy)
- **Model Factory**: 实现混合模型路由 (`ModelRouter`)：
  - 路由逻辑：根据任务复杂度分发给 Gemini 3 (Mock/Preview), Claude 3.5/3.7, 或 Gemini Flash Lite。

### 3. 多代理角色实现 (Agent Implementation)
- **Manager Agent (The Brain)**:
  - 职责：解析用户需求，生成 `Plan`，分发任务给 Editor/Verifier。
  - 工具：`SearchWeb`, `ManageContext`, `DelegateTask`.
- **Editor Agent (The Hands)**:
  - 职责：执行代码修改，文件操作，依赖安装。
  - 工具：`ReadFile`, `WriteFile`, `RunCommand` (Shell), `GitCommit`.
  - 机制：实现 Scope Isolation，仅能访问白名单目录。
- **Verifier Agent (The Eyes)**:
  - 职责：运行测试，执行浏览器自动化，反馈修复建议。
  - 工具：`RunTest`, `BrowserAction` (Playwright), `TakeScreenshot`.
  - 特性：集成 App Testing System，支持自动修复循环。

### 4. 自主循环与高级特性 (Autonomous Loops & Features)
- **ReAct & Reflection Loop**:
  - 实现 `Editor -> Verifier -> Manager` 的反馈闭环。
  - 错误发现后自动触发 `Fix` 流程。
- **Checkpoint & Rollback**:
  - 集成 LangGraph Checkpointer (SQLite/Postgres)。
  - 实现 Git 自动提交与回滚 (`git reset` 封装)。
- **Sandbox Environment**:
  - 封装 `ReplitEnv` 类，提供隔离的 Shell 执行环境。
  - 实现快照引擎 (Snapshot Engine) 的文件系统版本控制。

### 5. 前端交互界面 (Frontend Interface)
- **Chat Interface**: 支持多模态输入 (文本/截图)。
- **Artifact Viewer**: 实时查看代码变更、测试报告和预览 URL。
- **Control Panel**: 切换工作模式 (Build/Plan/Autonomy) 和查看 Agent 思考过程。

### 6. 执行路线图
1.  初始化项目骨架。
2.  构建 LangGraph 核心图结构与状态定义。
3.  实现三大 Agent 及其专属工具集。
4.  开发 Model Router 与混合模型策略。
5.  集成 Checkpoint 与自主循环逻辑。
6.  开发前端 UI 并联调。
