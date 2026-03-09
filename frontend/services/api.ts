const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export const buildImageUrl = (path: string) => `${API_BASE}${path}`;

export async function generateAvatar(formData: FormData) {
  const res = await fetch(`${API_BASE}/generate-avatar`, { method: "POST", body: formData });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function uploadClothes(formData: FormData) {
  const res = await fetch(`${API_BASE}/upload-clothes`, { method: "POST", body: formData });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function tryOn(avatar_image_url: string, clothes_image_url: string) {
  const res = await fetch(`${API_BASE}/try-on`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ avatar_image_url, clothes_image_url }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function generatePose(avatar_image_url: string, pose_type: string) {
  const res = await fetch(`${API_BASE}/generate-pose`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ avatar_image_url, pose_type }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getHistory() {
  const res = await fetch(`${API_BASE}/history`);
  return res.json();
}

export async function getAvatars() {
  const res = await fetch(`${API_BASE}/avatars`);
  return res.json();
}

export async function getClothes() {
  const res = await fetch(`${API_BASE}/clothes`);
  return res.json();
}
