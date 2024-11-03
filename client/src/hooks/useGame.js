import { useContext, useCallback, useState } from "react";
import { GameContext } from "../context/GameContext";

export const useGame = () => {
  const context = useContext(GameContext);
  const [selectedAttacker, setSelectedAttacker] = useState(null);

  if (!context) {
    throw new Error("useGame must be used within a GameProvider");
  }

  const { gameState, sendAction } = context;

  const playCard = useCallback(
    (cardIndex) => {
      sendAction({
        type: "play_card",
        card_index: cardIndex,
      });
    },
    [sendAction]
  );

  const selectAttacker = useCallback((index) => {
    setSelectedAttacker(index);
  }, []);

  const attack = useCallback(
    (attackerIndex, targetIndex) => {
      sendAction({
        type: "attack",
        attacker_index: attackerIndex,
        target_index: targetIndex,
      });
      setSelectedAttacker(null); // Clear selection after attack
    },
    [sendAction]
  );

  const endTurn = useCallback(() => {
    sendAction({
      type: "end_turn",
    });
    setSelectedAttacker(null); // Clear selection when ending turn
  }, [sendAction]);

  const cancelAttack = useCallback(() => {
    setSelectedAttacker(null);
  }, []);

  return {
    ...context,
    playCard,
    attack,
    endTurn,
    selectedAttacker,
    selectAttacker,
    cancelAttack,
  };
};
