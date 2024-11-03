import React from "react";
import { useGame } from "../../hooks/useGame";
import {
  Box,
  Button,
  Typography,
  CircularProgress,
  Container,
} from "@mui/material";

import PlayerBoard from "./PlayerBoard";
import OpponentBoard from "./OpponentBoard";

const GameBoard = () => {
  const { gameState, isLoading, error, startNewGame } = useGame();

  React.useEffect(() => {
    if (!gameState) {
      startNewGame();
    }
  }, [gameState, startNewGame]);

  if (isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress sx={{ color: "white" }} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        minHeight="100vh"
        gap={2}
      >
        <Typography color="error">{error}</Typography>
        <Button variant="contained" onClick={startNewGame}>
          Try Again
        </Button>
      </Box>
    );
  }

  if (!gameState) return null;

  const { current_player, opponent_player } = gameState;

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Opponent's Side */}
      <OpponentBoard player={opponent_player} />

      {/* Player's Side */}
      <PlayerBoard player={current_player} />
    </Container>
  );
};

export default GameBoard;
