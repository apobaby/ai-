import Link from "next/link";
import { ReactNode } from "react";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen">
      <nav className="bg-white shadow">
        <div className="mx-auto flex max-w-5xl gap-5 p-4 text-sm font-medium">
          <Link href="/">首页</Link>
          <Link href="/upload-clothes">上传衣服</Link>
          <Link href="/try-on">AI试衣</Link>
          <Link href="/history">历史记录</Link>
        </div>
      </nav>
      <main className="mx-auto max-w-5xl p-4">{children}</main>
    </div>
  );
}
