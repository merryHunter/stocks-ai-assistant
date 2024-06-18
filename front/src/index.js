import React from 'react';
import Chatbot from './Chatbot';
import { createRoot } from 'react-dom/client';

function App() {
  return (
    <div>
      <h1>Stocks AI Assistant</h1>
      <Chatbot />
    </div>
  );
}

const container = document.getElementById('root');
const root = createRoot(container); 
root.render(<App tab="home" />);
