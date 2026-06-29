/* iframe is an html element that acts like a window on your webpage, 
allowing you to embed a completely separate webpage or document
directly on the page you're viewing */
import styles from "./ArtistPage/ArtistPage.module.css"	
export default function YoutubeEmbed({ video, setVideo, videoIds }) {
  return (
<div>
    <iframe className={styles.video}
      src={`https://www.youtube.com/embed/${videoIds[video]}`}
      title="YouTube video player"
      allowFullScreen
    />

</div>
  );
}
