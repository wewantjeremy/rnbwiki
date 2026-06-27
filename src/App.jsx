import SideBar from './SideBar';
import ArtistPage from './ArtistPage';
import Header from './components/Header';
import { useState } from 'react';
import { artists } from "../artists";

function App() {
  const [selectedArtist, setSelectedArtist] = useState(artists[0]);

  return (
    <div className="container">
      <SideBar
        artists={artists}
        onSelect={setSelectedArtist}
      />

      <main className="main-content">
        <Header />
        <ArtistPage artist={selectedArtist} />
      </main>
    </div>
  );
}

export default App;