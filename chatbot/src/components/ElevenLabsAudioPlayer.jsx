import React, { useState } from 'react';

const AudioGenerator = () => {
    const [text, setText] = useState('');
    const [audioSrc, setAudioSrc] = useState('');

    const handleTextChange = (e) => {
        setText(e.target.value);
    };

    const generateAudio = async () => {
        try {
            const response = await fetch(`http://localhost:9001/voice/${text}`);
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            const data = await response.json();
            if (data.audio_base64) {
                const audioBlob = base64ToBlob(data.audio_base64, 'audio/mpeg');
                const audioUrl = URL.createObjectURL(audioBlob);
                setAudioSrc(audioUrl);
            } else {
                console.error('Error generating audio:', data.error);
            }
        } catch (error) {
            console.error('Error fetching audio:', error);
        }
    };
     // Helper function to convert base64 string to blob
     const base64ToBlob = (base64, mimeType) => {
        const byteCharacters = atob(base64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], {type: mimeType});
    };


    return (
        <div className="flex flex-col items-center justify-center p-4">
            <textarea
                className="w-full p-2 mb-4 border rounded shadow-sm focus:outline-none focus:ring focus:border-blue-300"
                value={text}
                onChange={handleTextChange}
                placeholder="Enter text to synthesize"
            />
            <button
                className="px-4 py-2 mb-4 text-white bg-blue-500 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50"
                onClick={generateAudio}
            >
                Generate Audio
            </button>
            {audioSrc && <audio controls src={audioSrc} autoPlay className="w-full mt-4" />}
        </div>
    );
};

export default AudioGenerator;
