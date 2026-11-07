import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://archive.example.com";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "Lumière Archive · 跨文明典藏索引",
    template: "%s · Lumière Archive",
  },
  description:
    "25 期「古代名人 · 书画长卷」数字展卷。逐件登记权利状态，署名与来源完整可见。",
  openGraph: {
    type: "website",
    siteName: "Lumière Archive",
    title: "Lumière Archive · 跨文明典藏索引",
    description:
      "以 IIIF 光栅流式传输呈现中国书画与西方绘画，逐件登记权利与来源。",
    url: SITE_URL,
    locale: "zh_CN",
  },
  twitter: {
    card: "summary_large_image",
    title: "Lumière Archive · 跨文明典藏索引",
    description: "以 IIIF 光栅流式传输呈现中国书画与西方绘画。",
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
