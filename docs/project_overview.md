# 專案總覽與框架

本文件提供 Blender Geometry Nodes MCP 外掛的整體藍圖，包含目標、核心模組、目錄結構與開發流程指南，作為後續實作與協作的導覽。

## 1. 產品目標
- 以聊天式 MCP 介面操控 Blender 幾何節點，支援快速探索、編輯與自動化視覺工程工作。
- 提供可擴充的能力宣告與安全保護欄，確保遠端操作透明且可審計。
- 以插件形式整合 Blender，兼容 headless/GUI 工作流程並支援範例腳本。

## 2. 核心構面
- **MCP 服務層**：提供 stdio 或 WebSocket 通訊，處理 list_capabilities、執行節點操作、回傳上下文快照與錯誤。
- **幾何節點語意層**：抽象 Blender 節點、連線與群組，提供序列化、差異計算與型別檢查。
- **插件整合層**：Addon 註冊、偏好設定、日誌、快捷操作與 UI 面板。
- **開發運維層**：打包、版本管理、測試自動化、範例與文件。

## 3. 建議目錄結構
下列骨架已建立，後續功能會在對應模組中補齊。

```
/ (專案根目錄)
├── README.md                      # 簡介與快速開始
├── docs/                          # 規劃、設計、任務與範例文件
│   ├── development_plan.md
│   ├── mcp_geometry_nodes.md
│   ├── project_overview.md
│   └── task_list.md
├── addon/                         # Blender 外掛主體
│   ├── __init__.py                # Addon 註冊、入口、偏好設定
│   ├── mcp_server.py              # MCP 通訊入口（stdio/WebSocket）
│   ├── capabilities.py            # list_capabilities 與能力宣告
│   ├── context_serializer.py      # 幾何節點上下文序列化與差異
│   ├── node_ops.py                # 節點增刪改連接與檢查
│   ├── ui/                        # 偏好設定、面板、快捷工具
│   └── tests/                     # 針對 addon 的單元/整合測試
├── scripts/                       # 頭less 測試與範例指令
├── examples/                      # MCP 互動範例與節點模板
├── tools/                         # 開發輔助工具、打包/發布腳本
└── CHANGELOG.md                   # 版本更新
```

## 4. 模組責任與邊界
- **mcp_server.py**：負責通訊、請求路由、錯誤處理、記錄稽核；提供 dry-run 支援。
- **capabilities.py**：宣告能力與參數結構，管理版本/兼容性旗標。
- **context_serializer.py**：輸出節點/連線/群組/選取狀態，支援差異快照與格式驗證。
- **node_ops.py**：執行節點操作，包含型別檢查、資料插槽驗證、回滾/預檢模式。
- **ui/**：偏好設定頁、Geometry Nodes 編輯器內工具區塊、快捷鍵/命令入口。
- **tests/**：Blender 內的單元測試與 headless 整合測試，覆蓋序列化與操作路由。

## 5. 里程碑與交付物對應
- **MVP**：完成 MCP 通訊骨架、能力宣告、上下文序列化 v1、基本節點 CRUD 與 dry-run。
- **UX 強化**：偏好設定、UI 面板、快捷鍵、範例腳本；擴充節點操作（群組、框架、靜音）。
- **品質與發布**：測試矩陣、打包腳本、CHANGELOG 與最低版本標示、教學文件。

## 6. 協作與開發流程
- 每次完成一組功能，更新 `docs/task_list.md` 的狀態與新增後續任務。
- 提交前確保文件與程式碼結構對齊；新增檔案需符合上述目錄命名。
- 測試與範例腳本置於 `scripts/`，正式測試置於 `addon/tests/`，文件統一放入 `docs/`。
