// src/context/GameContext.jsx
import React, { createContext, useState, useCallback } from "react";
import gameService from "../services/gameService";

export const GameContext = createContext(null);

export const GameProvider = ({ children }) => {
  const [gameState, setGameState] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const startNewGame = useCallback(async () => {
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
        await gameService.sendAction(sessionId, action);
        const newState = await gameService.getGameState(sessionId);
        setGameState(newState);
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
