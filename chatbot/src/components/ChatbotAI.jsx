import React, { useEffect, useState, useRef } from "react";
import { OpenAI } from "langchain/llms/openai";
import { BufferMemory } from "langchain/memory";
import { ConversationChain } from "langchain/chains";
import { SerpAPI } from "langchain/tools";
import RetrieveChunks from "./RetrieveChunks";

const ChatbotAI = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [showChunks, setShowChunks] = useState(false);
  const [initialResponse, setInitialResponse] = useState("Hi Albert! I'm Asif Qamar. How can I help you today?");
  const [serverUrl, setServerUrl] = useState("http://localhost:9000");
  const [elevenLabsUrl, setElevenLabsUrl] = useState("http://localhost:9001/voice/");
  const [EndPoint, setEndPoint] = useState("chunk");
  const [elevenLabsText, setElevenlabsText] = useState('');
  const [audioSrc, setAudioSrc] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [chunkQuery, setChunkQuery] = useState('');


  useEffect(() => {
    // Set the server URL from env variable or use the default
    setServerUrl(process.env.REACT_APP_SERVER_URL || serverUrl);
    setEndPoint(process.env.REACT_APP_ENDPOINT || EndPoint);
    setMessages([{ text: initialResponse, type: "bot" }]);
  }, []);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const generateChunks = async () => {
    console.log("Generate Chunks");
    setShowChunks(!showChunks); // Toggle the visibility of chunks
  };


  const handleClear = () => {
    console.log("Clear the chat");
    setMessages([]);
    setInputValue('');
    setChunkQuery('');
    //setMessages([{ text: initialResponse, type: 'bot' }]);
  };

  const handleSend = async () => {
    setSubmitted(true);
    if (inputValue.trim() !== '') {
      const url = `${serverUrl}/${EndPoint}/query=${inputValue}`;
      console.log(url);
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
      const botResponse = await response.json();
      if (botResponse.error) {
        throw new Error(`Error: ${botResponse.error}`);
      }
      console.log(botResponse);
      setElevenlabsText(botResponse);

      // Fetch the audio URL
      const audioUrl = await generateAudio(botResponse);
      if (audioUrl) {
        console.log(audioUrl);
        setAudioSrc(audioUrl);
        setMessages([...messages,
        { text: inputValue, type: 'user' },
        { text: botResponse, type: 'bot' },
        { audioUrl: audioUrl, type: 'bot' }
        ]);

      }

      // Update messages state with text and audio URL
      setChunkQuery(inputValue)

      setInputValue('');
      
    }
  };

  // Audio Generator

  const generateAudio = async (botResponse) => {
    try {
      const url = elevenLabsUrl + botResponse;
      console.log(url);
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
      const data = await response.json();
      if (data.audio_base64) {
        const audioBlob = base64ToBlob(data.audio_base64, 'audio/mpeg');
        return URL.createObjectURL(audioBlob);
      } else {
        console.error('Error generating audio:', data.error);
      }
    } catch (error) {
      console.error('Error fetching audio:', error);
    }
    return null; // Return null if there's an error or no audio
  };
  // Helper function to convert base64 string to blob
  const base64ToBlob = (base64, mimeType) => {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
  };




  return (
    <div className="w-auto h-auto border border-gray-600 flex flex-col justify-between">
      <div className="flex p-4 border-t border-gray-600">
        <h1 className="text-3xl font-bold">Chatbot- Powered by AI</h1>
      </div>
      <div className="p-4 overflow-y-auto">
        {messages.map((message, index) => (
          <div key={index} className={`mb-2 p-2 rounded ${message.type === "user" ? "bg-gray-200 ml-auto" : "bg-sky-500/100 shadow-lg shadow-sky-500/50"}`}>
            {message.text}

            {message.audioUrl && (
              <audio controls src={message.audioUrl}></audio>
            )}
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
        <button
          onClick={generateChunks}
          className="px-4 py-1 bg-sky-500/100 shadow-lg shadow-sky-500/100 rounded-full"
        >
          {showChunks ? "Hide Chunks" : "Generate Chunks"}
        </button>
      </div>
      {showChunks && <RetrieveChunks query={chunkQuery} />}
    </div>

  );
}

export default ChatbotAI