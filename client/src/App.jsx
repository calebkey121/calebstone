import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { GameProvider } from "./context/GameContext";

// Pages
import MainMenu from "./pages/MainMenu/MainMenu";
import GameBoard from "./components/Game/GameBoard";
import CardCollection from "./pages/CardCollection";

// Layout components
import Header from "./components/layout/Header";

function App() {
  return (
    <BrowserRouter>
      <GameProvider>
        <div className="min-h-screen bg-gradient-to-br from-purple-900 to-blue-900">
          <Header />
          <main className="h-full">
            <Routes>
              <Route path="/" element={<MainMenu />} />
              <Route path="/play" element={<GameBoard />} />
              <Route path="/cards" element={<CardCollection />} />
            </Routes>
          </main>
        </div>
      </GameProvider>
    </BrowserRouter>
  );
}

export default App;
