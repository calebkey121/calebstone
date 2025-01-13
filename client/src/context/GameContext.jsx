import React, { createContext, useState, useCallback } from "react";
import gameService from "../services/gameService";

export const GameContext = createContext(null);

export const GameProvider = ({ children }) => {
  const [gameState, setGameState] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const startNewGame = useCallback(async (e) => {
    if (e) e.preventDefault();
    try {
      setIsLoading(true);
      const { session_id } = await gameService.startNewGame();
      setSessionId(session_id);
      const state = await gameService.getGameState(session_id);
      setGameState(state);
      setError(null);
    } catch (err) {
      setError("Failed to start new game");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const sendAction = useCallback(
    async (action) => {
      if (!sessionId) return;

      try {
        setIsLoading(true);
        const { game_state } = await gameService.sendAction(sessionId, action);
        setGameState(game_state); // Update state directly from response
        setError(null);
      } catch (err) {
        setError("Failed to process action");
      } finally {
        setIsLoading(false);
      }
    },
    [sessionId]
  );

  const value = {
    gameState,
    sessionId,
    error,
    isLoading,
    startNewGame,
    sendAction,
  };

  return <GameContext.Provider value={value}>{children}</GameContext.Provider>;
};
