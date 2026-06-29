import YoutubeEmbed from '../YoutubeEmbed'
import { useState } from 'react'
import styles from '../ArtistPage/ArtistPage.module.css'


export default function VideoGallery({ videoIds }) {
  const [video, setVideo] = useState(0)
  return(
  <div className={styles.videoContainer}>
    <YoutubeEmbed
      video={video}
      setVideo={setVideo}
      videoIds={videoIds} />

    <button
      className={`${styles.arrow} ${styles.prev}`}
      onClick={() =>
        setVideo((video - 1 + videoIds.length) % videoIds.length)
      }
    >
      &#10094;
    </button>
    <button
      className={`${styles.arrow} ${styles.next}`}
      onClick={() =>
        setVideo((video + 1 + videoIds.length) % videoIds.length)
      }>
      &#10095;
    </button>
  </div>
  )
}