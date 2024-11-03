import React from "react";
import { useGame } from "../../hooks/useGame";
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Grid2,
  CircularProgress,
  Container,
  Chip,
  Stack,
} from "@mui/material";
import {
  SyncAlt as EndTurnIcon,
  Cancel as CancelIcon,
} from "@mui/icons-material";
import GameCard from "./GameCard";
import PlayerStats from "./PlayerStats";

const GameBoard = () => {
  const {
    gameState,
    isLoading,
    error,
    startNewGame,
    playCard,
    attack,
    endTurn,
    selectedAttacker,
    selectAttacker,
    cancelAttack,
  } = useGame();

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
      <Box mb={4}>
        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="center"
          mb={2}
        >
          <PlayerStats player={opponent_player} isOpponent />
          <Typography color="rgba(255,255,255,0.6)">
            Cards in hand: {opponent_player.hand.length}
          </Typography>
        </Box>

        <Grid2 container spacing={1}>
          {opponent_player.army.map((ally, index) => (
            <Grid2 item xs={1.5} key={index}>
              <GameCard card={ally} index={index} type="board" />
            </Grid2>
          ))}
        </Grid2>
      </Box>

      {/* Player's Side */}
      <Box mt={4}>
        <Grid2 container spacing={1} mb={2}>
          {current_player.army.map((ally, index) => (
            <Grid2 item xs={1.5} key={index}>
              <GameCard card={ally} index={index} type="board" />
            </Grid2>
          ))}
        </Grid2>

        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="center"
          mb={2}
        >
          <PlayerStats player={current_player} />

          <Stack direction="row" spacing={1}>
            {selectedAttacker !== null && (
              <Button
                variant="contained"
                color="error"
                startIcon={<CancelIcon />}
                onClick={cancelAttack}
              >
                Cancel Attack
              </Button>
            )}
            <Button
              variant="contained"
              color="primary"
              startIcon={<EndTurnIcon />}
              onClick={endTurn}
            >
              End Turn
            </Button>
          </Stack>
        </Box>

        <Grid2 container spacing={1}>
          {current_player.hand.map((card, index) => (
            <Grid2 item xs={1.5} key={index}>
              <GameCard card={card} index={index} type="hand" />
            </Grid2>
          ))}
        </Grid2>
      </Box>
    </Container>
  );
};

export default GameBoard;
