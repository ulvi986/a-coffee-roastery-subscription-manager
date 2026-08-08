import { useCallback, useEffect, useState } from 'react';
import { api, Item } from './api';

export default function App() {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [title, setTitle] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'done'>('all');
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    try {
      setItems(await api.listItems());
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  async function addItem(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || busy) return;
    setBusy(true);
    try {
      await api.createItem(title.trim());
      setTitle('');
      await load();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function toggle(item: Item) {
    try {
      await api.updateItem(item.id, { completed: !item.completed });
      await load();
    } catch (err: any) {
      setError(err.message);
    }
  }

  async function remove(id: number) {
    try {
      await api.deleteItem(id);
      await load();
    } catch (err: any) {
      setError(err.message);
    }
  }

  const visible = items.filter((i) => {
    if (filter === 'active') return !i.completed;
    if (filter === 'done') return i.completed;
    return true;
  });
  const openCount = items.filter((i) => !i.completed).length;

  return (
    <div className="shell">
      <header className="hero">
        <h1>A Coffee Roastery Subscription Manager</h1>
        <p>Create, organise and track your items — simple and fast.</p>
      </header>

      <main className="card">
        <form className="add-form" onSubmit={addItem}>
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            maxLength={300}
            aria-label="New item title"
          />
          <button type="submit" disabled={busy || !title.trim()}>Add item</button>
        </form>

        <div className="toolbar">
          <span className="count">{openCount} open · {items.length - openCount} done</span>
          <div className="filters">
            {(['all', 'active', 'done'] as const).map((f) => (
              <button key={f} className={filter === f ? 'active' : ''} onClick={() => setFilter(f)}>
                {f}
              </button>
            ))}
          </div>
        </div>

        {error && <div className="banner error">⚠️ {error}</div>}
        {loading ? (
          <p className="hint">Loading…</p>
        ) : visible.length === 0 ? (
          <div className="empty">
            <div className="empty-emoji">🗒️</div>
            <p>{items.length === 0 ? 'No items yet. Add your first one above!' : 'Nothing here.'}</p>
          </div>
        ) : (
          <ul className="item-list">
            {visible.map((item) => (
              <li key={item.id} className={item.completed ? 'done' : ''}>
                <label className="check">
                  <input type="checkbox" checked={item.completed} onChange={() => toggle(item)} />
                  <span className="box" />
                  <span className="title">{item.title}</span>
                </label>
                <button className="delete" onClick={() => remove(item.id)} aria-label="Delete item">✕</button>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}
