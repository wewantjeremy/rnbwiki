import { useState } from "react";
import styles from "./ArtistPage.module.css"
import ImageGallery from '../ImageGallery/ImageGallery.jsx'
import VideoGallery from "../VideoGallery/VideoGallery.jsx"
import Biography from '../Biography/Biography.jsx'
import Comment from '../Comment/Comment.jsx'
import artist from '../../data/112.js'


export default function ArtistPage() {
  return (
    <>
      <h1 className={styles.h1}>{artist.name}</h1>
      <ImageGallery images={artist.images} />
      <VideoGallery videoIds={artist.videoIds} />
      <Biography biography={artist.biography}
        albums={artist.albums}
      />
      <Comment />
    </>
  );
}