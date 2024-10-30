import React, { useState, useEffect } from "react";

const GameClient = () => {
  const [gameState, setGameState] = useState(null);
  const [selectedCard, setSelectedCard] = useState(null);
  const [selectedAttacker, setSelectedAttacker] = useState(null);

  // Simulate fetching initial game state
  useEffect(() => {
    fetchGameState();
  }, []);

  const fetchGameState = async () => {
    try {
      const response = await fetch("http://localhost:5000/game_state");
      const data = await response.json();
      setGameState(data);
    } catch (error) {
      console.error("Error fetching game state:", error);
    }
  };

  const sendAction = async (action) => {
    try {
      await fetch("http://localhost:5000/action", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(action),
      });
      fetchGameState(); // Refresh game state after action
    } catch (error) {
      console.error("Error sending action:", error);
    }
  };

  const handlePlayCard = (cardIndex) => {
    sendAction({
      type: "play_card",
      card_index: cardIndex,
    });
  };

  const handleAttack = (attackerIndex, targetIndex) => {
    sendAction({
      type: "attack",
      attacker_index: attackerIndex,
      target_index: targetIndex,
    });
  };

  const handleEndTurn = () => {
    sendAction({
      type: "end_turn",
    });
  };

  if (!gameState) return <div className="p-4">Loading game state...</div>;

  const currentPlayer = gameState.current_player;
  const opponentPlayer = gameState.opponent_player;

  return (
    <div className="p-4">
      {/* Opponent Section */}
      <div className="mb-6 p-4 border rounded">
        <h2 className="text-xl font-bold mb-2">Opponent</h2>
        <div className="mb-2">
          Gold: {opponentPlayer.gold} | Income: {opponentPlayer.income}
        </div>
        <div className="mb-2">
          Hero: {opponentPlayer.hero.name} | Health:{" "}
          {opponentPlayer.hero.health}
        </div>
        <div className="mb-2">
          Army:{" "}
          {opponentPlayer.army.map((ally, i) => (
            <button
              key={i}
              className="mr-2 p-2 border rounded hover:bg-gray-100"
              onClick={() =>
                selectedAttacker !== null && handleAttack(selectedAttacker, i)
              }
            >
              {ally.name} ({ally.attack}/{ally.health})
            </button>
          ))}
        </div>
      </div>

      {/* Current Player Section */}
      <div className="p-4 border rounded">
        <h2 className="text-xl font-bold mb-2">Your Turn</h2>
        <div className="mb-2">
          Gold: {currentPlayer.gold} | Income: {currentPlayer.income}
        </div>
        <div className="mb-2">
          Hero: {currentPlayer.hero.name} | Health: {currentPlayer.hero.health}
        </div>
        <div className="mb-4">
          Army:{" "}
          {currentPlayer.army.map((ally, i) => (
            <button
              key={i}
              className={`mr-2 p-2 border rounded hover:bg-gray-100 ${
                selectedAttacker === i ? "bg-blue-100" : ""
              }`}
              onClick={() => (ally.can_attack ? setSelectedAttacker(i) : null)}
            >
              {ally.name} ({ally.attack}/{ally.health})
              {ally.can_attack ? " ⚔️" : ""}
            </button>
          ))}
        </div>
        <div className="mb-4">
          Hand:{" "}
          {currentPlayer.hand.map((card, i) => (
            <button
              key={i}
              className="mr-2 p-2 border rounded hover:bg-gray-100"
              onClick={() => handlePlayCard(i)}
              disabled={card.cost > currentPlayer.gold}
            >
              {card.name} ({card.cost}) {card.attack}/{card.health}
            </button>
          ))}
        </div>
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          onClick={handleEndTurn}
        >
          End Turn
        </button>
      </div>
    </div>
  );
};

export default GameClient;
