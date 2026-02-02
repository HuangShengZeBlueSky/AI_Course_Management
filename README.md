# AI Course Management（项目化课程仓库）

本仓库用于公开展示课程路线、项目列表、每周安排与备课进度；课程以“项目”为单位推进，代码与资料沉淀在仓库中。

**课程看板（本周课表/备课进度）**：

- https://github.com/users/HuangShengZeBlueSky/projects/1

---

# 第一节课：AI工具应用入门指导会议总结

这是一场关于AI工具应用的入门指导会议。本次会议主要介绍了AI工具的基本使用方法、环境配置技巧以及代码管理规范。主讲人通过实例演示了如何利用AI辅助学习、项目开发和学术研究，旨在帮助考研学生快速掌握现代技术工具。

## 1. AI工具的使用与介绍
* **概览**：介绍了AI工具的重要性，特别是对于考研和毕业论文写作的帮助，推荐使用 Gemini 等AI工具。
* **Google AI Studio**：详细讲解了使用方法，包括模型选择、参数调整和提示词编写。
* **温度系数（Temperature）**：解释了其作用——温度越高，输出越发散；温度越低，输出越稳定。
* **Agent（智能体）**：介绍了概念和使用方法，以字节跳动的扣子平台为例，展示了如何创建和使用技能。
* **RAG（检索增强生成）**：讲解了系统的实现方法，包括工作流定义和可视化搭建。

## 2. 环境配置与管理
* **Conda**：介绍了环境的创建、激活和管理方法，强调了环境隔离的重要性。
* **Docker**：讲解了使用方法，包括镜像拉取、环境挂载和容器运行，解决了环境冲突问题。
* **云端开发**：推荐使用 GitHub Codespace 和 Google Colab 等云端环境，避免本地配置的麻烦。

## 3. 代码管理与协作
* **Git基础**：介绍了基本指令和功能，包括代码提交、分支管理和 Pull Request 的使用。
* **版本控制**：强调了代码版本管理的重要性，方便回溯和协作开发。

## 4. Linux与服务器管理
* **基本指令**：讲解了文件管理、进程查看和显卡指定等操作。
* **工具推荐**：介绍了 tmux 的使用方法，解决长时间运行任务时电脑休眠的问题。

## 5. 笔记与文档编写
* **Markdown**：推荐使用 Typora 或飞书云文档编写，支持代码块、公式和表格插入。
* **LaTeX**：介绍了使用方法，包括文献引用和图表插入，推荐使用 Overleaf 平台。

## 6. 脚本编写与实验管理
* **Bash脚本**：讲解了编写方法，用于批量运行实验和参数调优。
* **最佳实践**：强调了脚本的可扩展性，避免将参数硬编码在代码中。

## 7. AI基础知识
* **核心机制**：介绍了 Attention 机制的基本原理和公式，强调了其在AI中的重要性。
* **评估指标**：讲解了常见的指标，如准确率（Accuracy）、召回率（Recall）和 F1 分数。

## 8. 作业与任务
* **课后作业**：要求使用扣子平台创建一个智能体技能，并分享实现过程。

---

## 会议待办 (Action Items)

- [ ] 在项目中使用 Docker 容器来创建隔离的开发环境，以避免包版本冲突
- [ ] 学习和使用 conda 环境管理工具以提高项目开发效率
- [ ] 编写代码规范和验证示例以提高代码质量和学习效果
- [ ] 掌握使用 AI 生成公式和表格的功能以提高工作效率
- [ ] 使用 AI 工具进行会议内容的有效记录和管理
- [ ] 了解并使用 Linux 命令进行进程管理、显卡指定等操作以提高系统性能
- [ ] 在 AI 项目课程中，使用 git 进行代码管理和协作，以提高工作效率并满足导师的要求
- [ ] 学习并使用 docker 命令进行容器运行和镜像构建
---


## 我们学什么

- AI 基本知识、Python 基本知识
- 环境管理 / 开发工具 / Git / AI 辅助学习与编程
- 项目模块：CV、NLP、ML、Agent+工具调用、RAG
- 论文复现、实验与论文写作练习
- 不定期嘉宾专题

---

## 本周安排（对外展示）

> 仅展示课程主题与备课状态；不在公开页面记录学员姓名与收款信息。

<!-- WEEKLY_SCHEDULE_START -->
> 本表由 GitHub Actions 从 Projects 自动生成；请在看板里维护（字段：Week/Date/LessonNo/Topic/Status/Materials）。

| 周次 | 日期 | 课次 | 主题 | 备课状态 | 课件/代码 |
| --- | --- | ---: | --- | --- | --- |
| 2026-W06 | 2026-02-02 | 1 | git，ai基础知识，ai工具 | 🟩 已完成 | 邀请你加入飞书用户4680QG的组织，区号为 +86 的手机号可通过此链接 https://bcn3s76oway7.feishu.cn/invite/member/3281RRrZCng |
| 2026-W06 | 2026-02-03 | 2 | 上节课没上完的。知识点汇总 | 🟨 备课中 | 邀请你加入飞书用户4680QG的组织，区号为 +86 的手机号可通过此链接 https://bcn3s76oway7.feishu.cn/invite/member/3281RRrZCng |
| 2026-W06 | 2026-02-05 | 1 | 我的一个科研项目，大家可以贡献 | 🟨 备课中 | （待补） |
<!-- WEEKLY_SCHEDULE_END -->

---

## 项目列表（按项目推进）

建议学习路径：基础 → ML → CV/NLP → LLM → RAG → Agent。

- [基础知识模块](projects/fundamentals/README.md)
- [大模型 LLM 模块](projects/llm/README.md)
- [ML（传统机器学习）项目](projects/ml/README.md)
- [CV 项目](projects/cv/README.md)
- [NLP 项目](projects/nlp/README.md)
- [RAG 项目](projects/rag/README.md)
- [Agent + 工具调用项目](projects/agent-tools/README.md)

---

## 收费方式（按“项目”收费）

如果你不是按“课次”收费，而是按“项目包”收费，建议用下面这种对外口径：

- **一个项目 = 一个交付包**：项目目标、里程碑、作业与验收标准、代码评审/答疑范围
- **一个付费项目 = 一个私有仓库**：付费后获得对应私有仓库的访问权限（权限最精确）

可选的项目包字段（你可以在每个项目 README 里加一段“交付与验收”）：

- 周期（例如 2~4 周）
- 交付物（代码仓库、报告、展示 demo）
- 验收方式（PR review、指标、演示）

更细的“权限设置/如何给学员开权限”见：

- [docs/pricing-and-access.md](docs/pricing-and-access.md)

---

## 权限与隐私（重要）

- 本仓库建议作为 **公开主页**：展示路线图、项目列表、本周安排、公开资料。
- 任何包含学员信息/收款记录/私密课件/答案的内容，建议放到 **私有仓库** 或私有组织项目中。

具体怎么做（GitHub 协作者/组织团队/按项目开权限），见：

- [docs/pricing-and-access.md](docs/pricing-and-access.md)

---

## 资料与协作

- 路线图与每周计划：
	- [syllabus/roadmap.md](syllabus/roadmap.md)
	- [syllabus/week-plan.template.md](syllabus/week-plan.template.md)
- 每节课课件与代码沉淀：
	- [lessons/README.md](lessons/README.md)
- 作业与验收标准：
	- [assignments/README.md](assignments/README.md)
- 协作方式：
	- [CONTRIBUTING.md](CONTRIBUTING.md)

