// All HTTP calls to the backend live in this one file.
//
// Why a relative base path ("/notes") and not "http://localhost:8000/notes"?
// Because in production this React app is served BY nginx, on the same
// origin as the API (nginx reverse-proxies /notes/* to FastAPI -- see
// nginx.conf). A relative path means this code works unchanged whether
// it's loaded from http://localhost, your LAN IP, or an ngrok URL.
//
// During local development (npm run dev, no nginx involved yet), this
// relative path is made to work too -- see the `proxy` section added to
// vite.config.js, which forwards /notes requests from the dev server to
// FastAPI on port 8000 under the hood.
const BASE = "/notes";

async function request(path, options) {
  const res = await fetch(BASE + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  // DELETE returns 204 No Content -- there's no JSON body to parse.
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  list: () => request("/"),
  create: (content) =>
    request("/", { method: "POST", body: JSON.stringify({ content }) }),
  update: (id, content) =>
    request(`/${id}`, { method: "PUT", body: JSON.stringify({ content }) }),
  remove: (id) => request(`/${id}`, { method: "DELETE" }),
};
