import { useState, useEffect } from "react"
import styles from "./Comment.module.css"
export default function Comment(){
  const [name, setName] = useState("");
  const [text, setText] = useState("")
  const [comments, setComments] = useState([]);
  useEffect(() => {
  fetch("http://localhost:3001/api/comments/112")
    .then((response) => response.json())
    .then((data) => setComments(data));
}, []);
  async function handleSubmit(e) {
    e.preventDefault()

    const response = await fetch("http://localhost:3001/api/comments", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        artistId: "112",
        name,
        text,
      }),
    })

    const savedComment = await response.json()
    setComments(
      [
        ...comments, savedComment])
        setName("");
        setText("");
  }
return (
  <>
  <span className={styles.postComment}>Post</span>
    <form className={styles.commentForm} onSubmit={handleSubmit}>
      <textarea className={styles.input}
        placeholder="Your name"
        value={name}
        onChange={e => setName(e.target.value)}
      />

      <textarea 
        placeholder="Share your thoughts..."
        value={text}
        onChange={e => setText(e.target.value)}
      />

      <button type="submit" className={styles.postButton}>Post Comment</button>
    </form>

    {comments.map((comment, index) => (
      <div key={index}>
        <strong>Name: {comment.name}</strong>
        <p>Comment: {comment.text}</p>
      </div>
    ))}
  </>
)}