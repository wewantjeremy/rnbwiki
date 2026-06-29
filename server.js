// server.js
import express from "express";
import cors from "cors";
import sqlite3 from "sqlite3";

const app = express();
const db = new sqlite3.Database("./comments.db");

app.use(cors());
app.use(express.json());

db.run(`
  CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id TEXT NOT NULL,
    name TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

app.get("/api/comments/:artistId", (request, response) => {
  db.all(
    "SELECT * FROM comments WHERE artist_id = ? ORDER BY created_at DESC",
    [request.params.artistId],
    (error, rows) => {
      if (error) return response.status(500).json({ error: error.message });
      response.json(rows);
    }
  );
});

app.post("/api/comments", (request, response) => {
  const { artistId, name, text } = request.body;

  db.run(
    "INSERT INTO comments (artist_id, name, text) VALUES (?, ?, ?)",
    [artistId, name, text],
    function (error) {
      if (error) return response.status(500).json({ error: error.message });

      response.json({
        id: this.lastID,
        artist_id: artistId,
        name,
        text,
      });
    }
  );
});

app.listen(3001, () => {
  console.log("Server running on http://localhost:3001");
});