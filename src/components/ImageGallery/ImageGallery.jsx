import { useState } from 'react'
import styles from './ImageGallery.module.css'

export default function ImageGallery( {images} ){
  console.log("IMAGEGALLERY IMAGES:", images);
  const [slide, setSlide] = useState(0);
  return(
<div className={styles.galleryContainer}>
<img
  className={styles.galleryImage}
  src={encodeURI(
    `https://images.rnbwiki.com${images[slide].replace("/src/images", "")}`
  )}
/>
  <button
    className={`${styles.arrow} ${styles.prev}`}
    onClick={() => setSlide((slide + images.length - 1) % images.length)}
  >
    &#10094;
  </button>

  <button
    className={`${styles.arrow} ${styles.next}`}
    onClick={() => setSlide((slide + 1) % images.length)}
  >
    &#10095;
  </button>
</div>)
}