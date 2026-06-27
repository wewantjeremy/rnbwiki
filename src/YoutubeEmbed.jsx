/* iframe is an html element that acts like a window on your webpage, 
allowing you to embed a completely separate webpage or document
directly on the page you're viewing */
export default function YoutubeEmbed({ videoId }) {
  return (
    <div align="center">
    <iframe
      width="70%"
      height="600"
      src={`https://www.youtube.com/embed/${videoId}`}
      title="YouTube video player"
      allowFullScreen
      display="block"
    />
    </div>
  );
}
