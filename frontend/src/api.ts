async function request<T = any>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (res.status === 204) return null as T;
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.detail || body.error || `Request failed (${res.status})`);
  return body as T;
}

export interface Item {
  id: number;
  title: string;
  completed: boolean;
  createdAt: string;
}

export const api = {
  listItems: () => request<Item[]>('/api/items'),
  createItem: (title: string) => request('/api/items', { method: 'POST', body: JSON.stringify({ title }) }),
  updateItem: (id: number, patch: Partial<Pick<Item, 'title' | 'completed'>>) =>
    request(`/api/items/${id}`, { method: 'PATCH', body: JSON.stringify(patch) }),
  deleteItem: (id: number) => request(`/api/items/${id}`, { method: 'DELETE' }),
};
