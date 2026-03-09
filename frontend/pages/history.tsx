import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { buildImageUrl, getHistory } from "../services/api";

type HistoryItem = {
  id: number;
  result_url: string;
  created_at: string;
};

export default function HistoryPage() {
  const [items, setItems] = useState<HistoryItem[]>([]);

  useEffect(() => {
    getHistory().then(setItems);
  }, []);

  return (
    <Layout>
      <h1 className="mb-4 text-2xl font-bold">历史试衣记录</h1>
      <div className="grid gap-4 md:grid-cols-3">
        {items.map((item) => (
          <div key={item.id} className="rounded bg-white p-3">
            <img src={buildImageUrl(item.result_url)} alt={`history-${item.id}`} className="rounded" />
            <p className="mt-2 text-xs text-gray-500">{new Date(item.created_at).toLocaleString()}</p>
          </div>
        ))}
      </div>
    </Layout>
  );
}
