import styles from '../ArtistPage/ArtistPage.module.css'
export default function Biography({ biography, albums }) {
  return (
    <>
      <h4 className={styles.h4}>Biography</h4>
      {biography.map((segment, index) => (
        <p key={index} 
        className={styles.p}>{segment.text}</p>
      ))}

      <h3 className={styles.h3}>Discography</h3>

      <ul>{albums.map((album) => (
        <li key={album.title}><a href={album.link} target="_blank">{album.title} ({album.year})</a></li>
      ))}
      </ul>
    </>
  )
}
