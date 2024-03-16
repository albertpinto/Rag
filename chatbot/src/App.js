import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import About from "./pages/About";
import NotFound from "./pages/NotFound";
import Navbar from "./components/layout/Navbar";
import Footer from "./components/layout/Footer";
import ChatbotAI from './components/ChatbotAI';
import ElevenLabsAudioPlayer from './components/ElevenLabsAudioPlayer';
import Chatbot from './components/Chatbot';


function App() {
  return (
    <Router>
      <Navbar />
        <main className="container mx-auto px-3 pb-12">
          <Routes>
            <Route path="/" element={<Chatbot />} />
            <Route path="/speak" element={<ElevenLabsAudioPlayer />} />
            <Route path="/chat" element={<Chatbot/>} />
            <Route path="/chatAI" element={<ChatbotAI />} />
            <Route path="/notfound" element={<NotFound />} />
            <Route path="/about" element={<About />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
    </Router>
  );
}

export default App;
