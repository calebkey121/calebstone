import React from "react";
import { useGame } from "../../hooks/useGame";
import {
  Box,
  Button,
  Typography,
  CircularProgress,
  Stack,
} from "@mui/material";
import {
  SyncAlt as EndTurnIcon,
  Cancel as CancelIcon,
} from "@mui/icons-material";
import CardGrid from "./CardGrid";
import PlayerStats from "./PlayerStats";
import BoardContainer from "./BoardContainer";

const GameBoard = () => {
  const {
    gameState,
    isLoading,
    error,
    startNewGame,
    selectedAttacker,
    cancelAttack,
    endTurn,
  } = useGame();

  React.useEffect(() => {
    if (!gameState) {
      startNewGame();
    }
  }, [gameState, startNewGame]);

  if (isLoading) {
    return (
      <Box className="flex justify-center items-center min-h-screen">
        <CircularProgress className="text-white" />
      </Box>
    );
  }

  if (error) {
    return (
      <Box className="flex flex-col items-center justify-center min-h-screen gap-4">
        <Typography className="text-red-500">{error}</Typography>
        <Button variant="contained" onClick={startNewGame}>
          Try Again
        </Button>
      </Box>
    );
  }

  if (!gameState) return null;

  const { current_player, opponent_player } = gameState;

  return (
    <div className="container mx-auto px-4 py-8 space-y-6">
      <Stack direction="row" spacing={2}>
        <Box sx={{ flex: 1 }}>
          <Stack direction="column" spacing={2}>
            <Box sx={{ flex: 3 }}>
              <PlayerStats player={opponent_player} isOpponent={true} />
            </Box>
            <Box sx={{ flex: 1 }}>
              <Button
                variant="contained"
                color="primary"
                startIcon={<EndTurnIcon />}
                onClick={endTurn}
                fullWidth
              >
                End Turn
              </Button>
            </Box>
            <Box sx={{ flex: 3 }}>
              <PlayerStats player={current_player} />
            </Box>
          </Stack>
        </Box>
        <Box sx={{ flex: 6 }}>
          <Stack direction="column" spacing={2}>
            <BoardContainer title="Opponent's Board">
              <CardGrid
                cards={opponent_player.army}
                type="board"
                isOpponent={true}
              />
            </BoardContainer>
            <BoardContainer title="Your Board">
              <CardGrid cards={current_player.army} type="board" />
            </BoardContainer>
          </Stack>
        </Box>
      </Stack>

      <BoardContainer title="Your Hand">
        <CardGrid cards={current_player.hand} type="hand" />
      </BoardContainer>
    </div>
  );
};

export default GameBoard;
