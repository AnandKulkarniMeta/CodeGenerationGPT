import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatLogRef = useRef(null); // Ref to track the chat log div

  // Function to add a timeout for the request
  const timeout = (ms) => new Promise((_, reject) => 
    setTimeout(() => reject(new Error('Request timed out.')), ms)
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }]);

      try {
        // Set a 30-second timer (30000 ms) for the response
        const response = await Promise.race([
          axios.post('http://localhost:8000/predict', { message: input }),
          timeout(30000)  // Timeout after 30 seconds
        ]);

        // If the response arrives before the timeout, update the messages
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: response.data.response, sender: 'ai' }
        ]);
      } catch (error) {
        let errorMessage = error.message === 'Request timed out.'
          ? 'Request timed out. Please try again later.'
          : 'Error communicating with the AI. Please try again.';

        setMessages((prevMessages) => [
          ...prevMessages,
          { text: errorMessage, sender: 'ai' }
        ]);
      }

      setInput('');
    }
  };

  // Function to scroll to the bottom of the chat log
  useEffect(() => {
    if (chatLogRef.current) {
      chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
    }
  }, [messages]); // Trigger whenever messages array changes

  // Function to start a new chat by clearing the messages
  const handleNewChat = () => {
    setMessages([]);
  };

  return (
    <div className="App">
      <aside className="sidemenu">
        <div className="sidemenu-button" onClick={handleNewChat}>New Chat</div>
      </aside>
      <section className="chatbox">
        <div className="chat-log" ref={chatLogRef}>
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${msg.sender === 'user' ? '' : 'chat-message-server'}`}
            >
              <div className="avatar"></div>
              <div className="message">{msg.text}</div>
            </div>
          ))}
        </div>
        <div className="chat-input-holder">
          <form onSubmit={handleSubmit}>
            <textarea
              className="chat_input-textarea"
              placeholder="Start typing..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              rows="3"
            />
            <button type="submit" className="chat_submit-button">
              <img src={require('./assets/message.png')} alt="Submit" className="submit-icon" />
            </button>
          </form>
        </div>
      </section>
    </div>
  );
}

export default App;
