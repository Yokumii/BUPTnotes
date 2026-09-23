# BUPTnotes

BUPTnotes 是一份面向北京邮电大学计算机相关课程的个人学习笔记，使用 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 构建。

在线阅读：[buptwiki.yokumi.cn](https://buptwiki.yokumi.cn)

## 内容

目前涵盖计算导论、离散数学、数据结构、数字逻辑、计算机组成原理、计算机网络、操作系统、数据库、编译原理、算法设计、计算机系统结构等课程。

部分内容由原始笔记经 LLM 辅助整理，可能存在错误或遗漏，请结合教材和课程资料审慎参考。

## 本地预览

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install mkdocs-material
mkdocs serve
```

访问终端输出的本地地址即可预览。站点导航和主题配置位于 `mkdocs.yml`，正文位于 `docs/`。

## 参与完善

欢迎通过 Issue 报告内容错误，或提交 Pull Request 补充和修正文档。请尽量注明课程、章节及参考来源。

## 许可证

本仓库中的原创内容和代码采用 [MIT License](LICENSE) 发布。引用材料的权利仍归原作者或原权利人所有。
