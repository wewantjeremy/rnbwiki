import { artists } from '../artists.js'
import styles from "./SideBar.module.css"

export default function SideBar ({ artists, onSelect }) { 
return (
  <aside className="sidebar">
    <ul className="sidebar-list">
      {artists.map((artist) => (
        <li className={styles.li} key={artist.id}
        onClick={() => onSelect(artist)}>
        {artist.name}</li>
      ))}     
    </ul>
  </aside>
  )
  }
