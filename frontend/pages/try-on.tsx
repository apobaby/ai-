import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { buildImageUrl, getAvatars, getClothes, tryOn } from "../services/api";

type ImageItem = { id: number; image_url: string };

export default function TryOnPage() {
  const [avatars, setAvatars] = useState<ImageItem[]>([]);
  const [clothes, setClothes] = useState<ImageItem[]>([]);
  const [avatar, setAvatar] = useState("");
  const [cloth, setCloth] = useState("");
  const [result, setResult] = useState("");

  useEffect(() => {
    getAvatars().then(setAvatars);
    getClothes().then(setClothes);
  }, []);

  const onTryOn = async () => {
    const res = await tryOn(avatar, cloth);
    setResult(res.result_image_url);
  };

  return (
    <Layout>
      <h1 className="mb-4 text-2xl font-bold">AI虚拟试衣</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded bg-white p-4">
          <h2 className="mb-2 font-semibold">选择数字模特</h2>
          <select className="w-full border p-2" value={avatar} onChange={(e) => setAvatar(e.target.value)}>
            <option value="">请选择</option>
            {avatars.map((a) => (
              <option key={a.id} value={a.image_url}>{`Avatar #${a.id}`}</option>
            ))}
          </select>
        </div>
        <div className="rounded bg-white p-4">
          <h2 className="mb-2 font-semibold">选择衣服</h2>
          <select className="w-full border p-2" value={cloth} onChange={(e) => setCloth(e.target.value)}>
            <option value="">请选择</option>
            {clothes.map((c) => (
              <option key={c.id} value={c.image_url}>{`Clothes #${c.id}`}</option>
            ))}
          </select>
        </div>
      </div>
      <button className="mt-4 rounded bg-blue-600 px-4 py-2 text-white" disabled={!avatar || !cloth} onClick={onTryOn}>
        生成试衣效果
      </button>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        {avatar && <img src={buildImageUrl(avatar)} alt="avatar" className="rounded bg-white p-2" />}
        {cloth && <img src={buildImageUrl(cloth)} alt="cloth" className="rounded bg-white p-2" />}
        {result && <img src={buildImageUrl(result)} alt="result" className="rounded bg-white p-2" />}
      </div>
    </Layout>
  );
}
