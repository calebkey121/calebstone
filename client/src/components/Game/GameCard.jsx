import React from "react";
import { useGame } from "../../hooks/useGame";

const GameCard = ({ card, index, isOpponent = false, type = "hand" }) => {
  const { selectedAttacker, selectAttacker, attack, playCard, gameState } =
    useGame();

  const handleClick = () => {
    if (type === "hand") {
      if (card.cost <= gameState.current_player.gold) {
        playCard(index);
      }
      return;
    }

    if (isOpponent && selectedAttacker !== null) {
      attack(selectedAttacker, index);
      return;
    }
    if (card.can_attack && !isOpponent) {
      selectAttacker(index);
    }
  };

  const isPlayable =
    type === "hand"
      ? card.cost <= gameState.current_player.gold
      : card.can_attack || (selectedAttacker !== null && isOpponent);

  const isSelected = type === "board" && selectedAttacker === index;

  return (
    <div
      className={`
        relative rounded-lg p-4
        ${
          isPlayable
            ? "cursor-pointer opacity-100"
            : "cursor-default opacity-70"
        }
        ${isSelected ? "border-2 border-blue-400" : "border border-white/20"}
        bg-white/10 backdrop-blur-md
        hover:bg-white/15
        ${
          isOpponent && selectedAttacker !== null
            ? "hover:border-red-500"
            : "hover:border-blue-400"
        }
        group
      `}
      onClick={handleClick}
    >
      <div className="space-y-2">
        <div className="flex justify-between items-start">
          <h3 className="text-white text-sm font-medium truncate">
            {card.name}
          </h3>
          <span className="inline-flex items-center justify-center h-5 min-w-[20px] px-1.5 text-xs text-white bg-white/20 rounded">
            {card.cost}
          </span>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-red-400 text-xs">⚔️ {card.attack}</span>
          <span className="text-green-400 text-xs">❤️ {card.health}</span>
        </div>

        {card.text && (
          <div
            className={`
              absolute left-0 right-0 bottom-full mb-2 p-2 
              bg-gray-900/95 rounded-lg text-sky-300 text-xs
              transform opacity-0 scale-95
              group-hover:opacity-100 group-hover:scale-100
              transition-all duration-200
              z-10 mx-2
            `}
          >
            {card.text}
          </div>
        )}
      </div>
    </div>
  );
};

export default GameCard;
