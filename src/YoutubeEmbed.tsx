/* iframe is an html element that acts like a window on your webpage, 
allowing you to embed a completely separate webpage or document
directly on the page you're viewing */
export default function YouTubeEmbed({ videoId }: { videoId: string }) {
  return (
    <iframe
      width="100%"
      height="315"
      src={`https://www.youtube.com/embed/${videoId}`}
      title="YouTube video player"
      allowFullScreen
    />
  );
}
