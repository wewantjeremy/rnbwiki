const images = Array.from(
  { length: artist.imageCount },
  (_, i) => `/images/${artist.id}/${i + 1}.jpg`
);