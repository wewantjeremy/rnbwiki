/* iframe is an html element that acts like a window on your webpage, 
allowing you to embed a completely separate webpage or document
directly on the page you're viewing */
import styles from "./ArtistPage.module.css"
	
const videoIds = ['8dtzMPApA4M', "ynMnPGmhsG0", 'GVOqbskGeBs', 'wl2NCXzg1FQ', 'IihCzGUEPbs', 'xM5g3tliVU0', 'XfiXby489Rk']
export default function YoutubeEmbed({ video, setVideo }) {
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
