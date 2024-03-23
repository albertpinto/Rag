import React, { useState } from 'react';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [serverUrl, setServerUrl] = useState(process.env.REACT_APP_ENDPOINT);
  const [botResponse, setBotResponse] = useState("");


  const handleSend = async () => {
    if (inputValue.trim() !== '') {
      const url = `${serverUrl}/prompt/${inputValue}`;
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const botResponseJson = await response.json();
        if (botResponseJson.error) {
          throw new Error(`Error: ${botResponseJson.error}`);
        }

        const botResponseText = botResponseJson // Accessing the 'response' field from the JSON
        const delimiter = "Critique agent's response:";
        const [agentsResponse, critique] = botResponseText.split(delimiter).map(part => part.trim());
        setMessages([...messages,
          { text: inputValue, type: 'user' },
          { text: "Agent's reponse:" + agentsResponse, type: 'bot' }, // Using the extracted 'response' value
          { text: "Critic Agent's Reponse:"+ critique, type: 'bot' } 
        ]);
      } catch (error) {
        console.error("Fetching error:", error);
  }
    }
    setInputValue('');
  };
  
  const handleClear = () => {
    setMessages([]);
  }

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }



  return (
    <div className="w-auto h-auto border border-gray-600 flex flex-col justify-between">
      <div className="flex p-4 border-t border-gray-600">
        <h1 className="text-3xl font-bold">Chatbot- Powered by AI</h1>
      </div>
      <div className="p-4 overflow-y-auto">
        {messages.map((message, index) => (
          <div key={index} className={`mb-2 p-2 rounded ${message.type === "user" ? "bg-gray-200 ml-auto" : "bg-sky-500/100 shadow-lg shadow-sky-500/50"}`}>
            {message.text}
          </div>
        ))}
      </div>
      <div className="flex p-4 border-t border-gray-600">
        <input
          value={inputValue}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          className="flex-1 p-2 border border-gray-600 rounded mr-2"
        />
        <button
          onClick={handleClear}
          className="px-4 py-1 bg-sky-500/100  shadow-lg shadow-sky-500/100 rounded-full"
        >
          Clear
        </button>
        <button
          onClick={handleSend}
          className="px-4 py-1 bg-sky-500/100 shadow-lg shadow-sky-500/100 rounded-full"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
