# Web 端（Next.js）

## 快速看版式（无需 Node）

直接用浏览器打开 `preview.html`——它是静态还原稿，与正式页面共用同一份
`app/globals.css` 和 `data/artworks.json`，由 `tools/build_web_preview.py` 生成。

> `preview.html` 是**查看用**，不是产物，不要直接部署。

## 正式运行

```bash
cd web
npm install        # 首次需要，会生成 package-lock.json，请一并提交
npm run dev        # http://localhost:3000
```

生产构建：

```bash
npm run build && npm start
```

## 数据来源

页面不直接读 CSV。`data/artworks.json` 由清单生成：

```bash
python3 ../tools/build_web_content.py   # CSV → JSON
python3 ../tools/build_web_preview.py   # JSON + CSS → preview.html
```

改了 `content/rights/artworks.csv` 之后要重跑第一条，否则页面数据是旧的。

## 设计来源

版式来自 Google Stitch 稿（`Lumière Archive`），做了三处调整：

1. 移除「个人典藏」——一期没有账号体系
2. 所有数字改为从内容库实时计算，不再写死
3. 图片位置改为占位块——原始稿是 AI 生成的仿作，不能用于真品展示

## 待办

- [ ] 自托管字体（Bodoni Moda / Inter），去掉对系统字体的依赖
- [ ] 接入真实 IIIF 图像（等 `image_url` 登记完成）
- [ ] 作品详情页 + 深缩放视图
- [ ] OG 卡片用真实作品图生成
