# 專案開發任務清單

建立可循序執行、可更新的任務清單，讓代理能逐步完成整個 Blender Geometry Nodes MCP 外掛開發。完成任務後請將該項目移至「已完成」，
並在必要時新增後續任務。

## 待完成
- [ ] 核對 MCP 通訊需求並決定初版傳輸方式（stdio 或 WebSocket），給出選擇理由與安全性注意事項。
- [ ] 建立 Blender 外掛骨架：`__init__.py`、註冊/反註冊、偏好設定與日誌基礎設計。
- [ ] 實作 MCP 請求路由與能力宣告（list_capabilities），包含參數模式與錯誤回應格式。
- [ ] 完成幾何節點上下文序列化：節點、連線、選取狀態、群組遞迴，以及可選的差異輸出。
- [ ] 提供節點編輯操作（新增、刪除、連接、設值、靜音/取消靜音、複製群組與框架），並加入型別檢查與 dry-run 機制。
- [ ] 建立 UI/UX：偏好設定頁面、Geometry Nodes 編輯器狀態面板、觸發上下文快照的快捷操作。
- [ ] 撰寫測試與範例腳本：頭less Blender 測試流程、節點序列化驗證、指令執行與回應示例。
- [ ] 打包與發佈流程：版本號規劃、CHANGELOG 範本、最低支援 Blender 版本確認。

## 已完成
- [x] 初版開發計畫與 MCP 能力草案（見 `docs/development_plan.md` 與 `docs/mcp_geometry_nodes.md`）。
- [x] 專案總覽與目錄架構框架（見 `docs/project_overview.md`）。
- [x] 建立建議目錄骨架（新增 `addon/`, `scripts/`, `examples/`, `tools/` 與占位檔）。
