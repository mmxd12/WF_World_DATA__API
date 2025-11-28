# WF_World_DATA_API
---

## 项目简介

`WF_World_DATA_API` 是一个用于获取 Warframe 游戏内数据的 API 服务项目。它为开发者提供了便捷的接口以访问游戏内各种物品、任务、赏金等信息。

## 🌟 功能特性

- ✅ 实时警报信息监控
- ✅ 入侵任务追踪
- ✅ 突击任务显示
- ✅ 虚空裂隙状态
- ✅ 虚空商人Baro Ki'Teer行程
- ✅ 午夜电波挑战任务
- ✅ 集团任务信息
- ✅ 开放世界赏金任务
- ✅ 九重天虚空风暴
- ✅ 执行官猎杀任务
- ✅ 完整的中文本地化支持

### 克隆仓库（可选）：
   ```bash
   git clone https://github.com/mmxd12/WF_World_DATA_API.git
   cd WF_World_DATA_API
   ```
## 📊 数据来源

使用Warframe官方API：`https://content.warframe.com/dynamic/worldState.php`

### 📁 配置文件

- `warframe_monitor.py` - 主程序文件
- `wfdata.json` - 游戏内名称映射
- `node.json` - 节点位置映射  
- `dict_zh.json` - 挑战任务中文翻译
- `ExportBounties.json` - 赏金任务映射
通常叫字典文件，用于将游戏内英文名称映射为中文名称，方便用户理解。

## 🤝 贡献指南

我们欢迎社区贡献！如果你希望为项目做贡献，请遵循以下步骤：

1. Fork 本仓库。
2. 创建新分支并提交你的修改。
3. 确保修改后的代码通过测试。
4. 提交 Pull Request。

## 其他事项
- 本项目仅供学习和研究使用，请勿用于商业用途。
- 本项目不隶属于 Digital Extremes 或 Warframe 官方。
- 本项目的字典文件并不是全面覆盖所有游戏内物品，仅包含常用或重要的部分。

## 外部链接
如果你想补全或更新字典文件，可以参考以下资源：
- [Warframe Wiki](https://wiki.warframe.com/w/Public_Export#Generic_Entry_Schema) # Warframe 官方维基的导出数据
- [WFCD/warframe-worldstate-data](https://github.com/WFCD/warframe-worldstate-data) # 推荐的一个开源数据仓库
- [browse](https://browse.wf/) # 这个网址的数据也很全面不过需要科学上网
- [Warframe Market](https://warframe.market/) # Warframe 第三方市场网站
- [calamity-inc/warframe-public-export-plus](https://github.com/calamity-inc/warframe-public-export-plus) # 跟第二个类似的开源数据仓库
#### git上的WFCD和calamity-inc他们还有其他的数据仓库可以参考，可以自行搜索。
---
