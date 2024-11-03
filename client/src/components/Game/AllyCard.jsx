import React from "react";
import { useGame } from "../../hooks/useGame";

const AllyCard = ({ ally, index, isOpponent = false }) => {
  const { selectedAttacker, selectAttacker, attack } = useGame();

  const handleClick = () => {
    // If we're the opponent and there's a selected attacker, we're being attacked
    if (isOpponent && selectedAttacker !== null) {
      attack(selectedAttacker, index);
      return;
    }

    // If we can attack and we're not the opponent, we're selecting an attacker
    if (ally.can_attack && !isOpponent) {
      selectAttacker(index);
    }
  };

  return (
    <div
      className={`
        relative rounded-lg p-4
        ${
          ally.can_attack || (selectedAttacker !== null && isOpponent)
            ? "cursor-pointer opacity-100"
            : "cursor-default opacity-70"
        }
        ${
          selectedAttacker === index
            ? "border-2 border-blue-400"
            : "border border-white/20"
        }
        bg-white/10 backdrop-blur-md
        hover:bg-white/15
        ${
          isOpponent && selectedAttacker !== null
            ? "hover:border-red-500"
            : "hover:border-blue-400"
        }
      `}
      onClick={handleClick}
    >
      <div className="space-y-2">
        <h3 className="text-white text-sm font-medium truncate">{ally.name}</h3>

        <div className="flex justify-between items-center">
          <span className="text-red-400 text-xs">⚔️ {ally.attack}</span>
          <span className="text-green-400 text-xs">❤️ {ally.health}</span>
        </div>
      </div>
    </div>
  );
};

export default AllyCard;
