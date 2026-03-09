import { FormEvent, useState } from "react";
import Layout from "../components/Layout";
import { buildImageUrl, uploadClothes } from "../services/api";

export default function UploadClothesPage() {
  const [clothes, setClothes] = useState<string>("");

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const res = await uploadClothes(formData);
    setClothes(res.clothes_image_url);
  };

  return (
    <Layout>
      <h1 className="mb-4 text-2xl font-bold">上传衣服</h1>
      <form className="rounded bg-white p-4" onSubmit={onSubmit}>
        <input name="clothes_image" type="file" accept="image/*" required />
        <button className="ml-3 rounded bg-blue-600 px-4 py-2 text-white">上传</button>
      </form>
      {clothes && <img src={buildImageUrl(clothes)} alt="clothes" className="mt-4 max-h-[500px] rounded bg-white p-2" />}
    </Layout>
  );
}
