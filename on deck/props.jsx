//Parent Component:jsxfunction 
  App() {
  return <WelcomeMessage name="Sarah" />;
}
//Child Component:
//The WelcomeMessage component receives those properties as an object parameter, typically named props.jsx
function WelcomeMessage(props) {
  return <h1>Hello, {props.name}</h1>; 
}

//destructured

//Parent Component:Pass multiple attributes to the child component just like HTML attributes.jsx
function App() {
  return (
    <UserProfile 
      username="Alex99" 
      age={27} 
      isAdmin={true} 
    />
  );
}

//Child Component (with Destructuring):Extract the properties directly inside the function argument parentheses { } instead of using the props keyword.jsx
function UserProfile({ username, age, isAdmin }) {
  return (
    <div>
      <h2>User: {username}</h2>
      <p>Age: {age}</p>
      <p>Role: {isAdmin ? "Administrator" : "Standard User"}</p>
    </div>
  );
}

//shared children 

import { useState } from 'react';

// Common Parent Component
function Parent() {
  // 1. Parent holds the shared state
  const [sharedText, setSharedText] = useState("");

  return (
    <div style={{ padding: '20px', border: '1px solid black' }}>
      <h1>Parent</h1>
      {/* 2. Pass the setter function to the sender child */}
      <InputChild setSharedText={setSharedText} />
      
      {/* 3. Pass the data to the receiver child */}
      <DisplayChild sharedText={sharedText} />
    </div>
  );
}

// Child B: The Sender (Changes the data)
function InputChild({ setSharedText }) {
  return (
    <div style={{ background: '#f0f0f0', padding: '10px', margin: '10px 0' }}>
      <h3>Child A (Sender)</h3>
      <input 
        type="text" 
        placeholder="Type something..." 
        onChange={(e) => setSharedText(e.target.value)} 
      />
    </div>
  );
}

// Child A: The Receiver (Displays the data)
function DisplayChild({ sharedText }) {
  return (
    <div style={{ background: '#e0e0e0', padding: '10px', margin: '10px 0' }}>
      <h3>Child B (Receiver)</h3>
      <p>Data received from sibling: <strong>{sharedText || "(empty)"}</strong></p>
    </div>
  );
}
