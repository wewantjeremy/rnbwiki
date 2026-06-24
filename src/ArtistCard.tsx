function ArtistCard({ artist }) {
  return (
    <div>
      <h2>{artist.name}</h2>
      {artist.youtubeId && (
        <iframe
          src={`https://www.youtube.com/embed/${artist.youtubeId}`}
          title={artist.name}
        />
      )}
    </div>
  );
}