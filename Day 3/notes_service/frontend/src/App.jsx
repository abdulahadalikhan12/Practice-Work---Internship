import { useState, useEffect } from "react";
import { api } from "./api";
import "./App.css";

function App() {
  const [notes, setNotes] = useState([]);
  const [draft, setDraft] = useState("");
  const [error, setError] = useState(null);

  // Runs once when the component first mounts (empty dependency array
  // at the end). This is how we "load notes on page load" in React --
  // there's no equivalent of the old fetchNotes() call sitting at the
  // bottom of a plain <script> tag; it has to be explicitly triggered
  // as a side effect like this.
  useEffect(() => {
    loadNotes();
  }, []);

  async function loadNotes() {
    try {
      const data = await api.list();
      setNotes(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleCreate() {
    const content = draft.trim();
    if (!content) return;
    try {
      await api.create(content);
      setDraft("");
      loadNotes();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleEdit(note) {
    const updated = window.prompt("Edit note:", note.content);
    if (updated === null) return; // user cancelled
    try {
      await api.update(note.id, updated);
      loadNotes();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm("Delete this note?")) return;
    try {
      await api.remove(id);
      loadNotes();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="app">
      <h1>My Notes</h1>

      <textarea
        className="note-input"
        rows={3}
        placeholder="Write a note..."
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
      />
      <button className="add-btn" onClick={handleCreate}>
        Add Note
      </button>

      {error && <div className="error-banner">{error}</div>}

      {notes.length === 0 && !error && (
        <p className="empty-state">No notes yet.</p>
      )}

      {notes
        .slice()
        .reverse()
        .map((note) => (
          <div className="note-card" key={note.id}>
            <div>{note.content}</div>
            <small>{new Date(note.created_at).toLocaleString()}</small>
            <div className="note-actions">
              <button onClick={() => handleEdit(note)}>Edit</button>
              <button onClick={() => handleDelete(note.id)}>Delete</button>
            </div>
          </div>
        ))}
    </div>
  );
}

export default App;
