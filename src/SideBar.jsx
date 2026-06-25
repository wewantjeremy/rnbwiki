import { artists } from '../artists.js'

export default function SideBar () { 
return (
  <aside className="sidebar">
    <ul>
      {artists.map((artist) => (
        <li key={artist.id}>{artist.name}</li>
      ))}     
    </ul>
  </aside>
  )
  }
