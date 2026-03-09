import { FormEvent, useState } from "react";
import Layout from "../components/Layout";
import { buildImageUrl, generateAvatar, generatePose } from "../services/api";

export default function Home() {
  const [avatar, setAvatar] = useState<string>("");
  const [pose, setPose] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      const formData = new FormData(e.currentTarget);
      const res = await generateAvatar(formData);
      setAvatar(res.avatar_image_url);
    } finally {
      setLoading(false);
    }
  };

  const onPose = async (poseType: string) => {
    if (!avatar) return;
    const res = await generatePose(avatar, poseType);
    setPose(res.pose_image_url);
  };

  return (
    <Layout>
      <h1 className="mb-4 text-2xl font-bold">数字模特生成</h1>
      <form className="space-y-3 rounded bg-white p-4" onSubmit={onSubmit}>
        <input name="user_image" type="file" accept="image/*" required />
        <input name="height" type="number" placeholder="身高(cm)" className="w-full border p-2" required />
        <input name="weight" type="number" placeholder="体重(kg)" className="w-full border p-2" required />
        <select name="gender" className="w-full border p-2" required>
          <option value="">选择性别</option>
          <option value="male">男</option>
          <option value="female">女</option>
          <option value="other">其他</option>
        </select>
        <button className="rounded bg-blue-600 px-4 py-2 text-white" disabled={loading}>
          {loading ? "生成中..." : "生成数字模特"}
        </button>
      </form>

      {avatar && (
        <div className="mt-4 rounded bg-white p-4">
          <img src={buildImageUrl(avatar)} alt="avatar" className="max-h-[500px] rounded" />
          <div className="mt-3 flex gap-2">
            <button className="rounded bg-slate-700 px-3 py-1 text-white" onClick={() => onPose("standing")}>standing</button>
            <button className="rounded bg-slate-700 px-3 py-1 text-white" onClick={() => onPose("walking")}>walking</button>
            <button className="rounded bg-slate-700 px-3 py-1 text-white" onClick={() => onPose("side view")}>side view</button>
          </div>
        </div>
      )}

      {pose && (
        <div className="mt-4 rounded bg-white p-4">
          <h2 className="mb-2 text-lg font-semibold">姿态生成结果</h2>
          <img src={buildImageUrl(pose)} alt="pose" className="max-h-[500px] rounded" />
        </div>
      )}
    </Layout>
  );
}
