import { useState } from "react"
import styles from "./Comment.module.css"
export default function Comment(){
  const [name, setName] = useState("");
  const [text, setText] = useState("")
  const [comments, setComments] = useState([]);
  function handleSubmit(e) {
    e.preventDefault()
    setComments(
      [
        ...comments,
        { name, text }
      ]
    )
  }
return (
  <>
  <span className={styles.textarea}>Post</span>
    <form className={styles.commentForm} onSubmit={handleSubmit}>
      <input
        placeholder="Your name"
        value={name}
        onChange={e => setName(e.target.value)}
      />

      <textarea
        placeholder="Share your thoughts..."
        value={text}
        onChange={e => setText(e.target.value)}
      />

      <button type="submit">Post Comment</button>
    </form>

    {comments.map((comment, index) => (
      <div key={index}>
        <strong>Name: {comment.name}</strong>
        <p>Comment: {comment.text}</p>
      </div>
    ))}
  </>
)}