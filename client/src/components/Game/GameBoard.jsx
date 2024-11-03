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
import AllyCard from "./AllyCard";
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
              <AllyCard ally={ally} index={index} isOpponent />
            </Grid2>
          ))}
        </Grid2>
      </Box>

      {/* Player's Side */}
      <Box mt={4}>
        <Grid2 container spacing={1} mb={2}>
          {current_player.army.map((ally, index) => (
            <Grid2 item xs={1.5} key={index}>
              <AllyCard ally={ally} index={index} />
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
              <Card
                sx={{
                  bgcolor: "rgba(255, 255, 255, 0.1)",
                  backdropFilter: "blur(10px)",
                  cursor:
                    card.cost <= current_player.gold ? "pointer" : "default",
                  opacity: card.cost <= current_player.gold ? 1 : 0.5,
                  "&:hover": {
                    borderColor: "#66bb6a",
                    bgcolor: "rgba(255, 255, 255, 0.15)",
                  },
                }}
                onClick={() =>
                  card.cost <= current_player.gold && playCard(index)
                }
              >
                <CardContent sx={{ p: 1, "&:last-child": { pb: 1 } }}>
                  <Box
                    display="flex"
                    justifyContent="space-between"
                    alignItems="start"
                    mb={1}
                  >
                    <Typography variant="subtitle2" color="white" noWrap>
                      {card.name}
                    </Typography>
                    <Chip
                      label={card.cost}
                      size="small"
                      sx={{
                        bgcolor: "rgba(255,255,255,0.2)",
                        color: "white",
                        height: "20px",
                      }}
                    />
                  </Box>
                  <Stack direction="row" justifyContent="space-between">
                    <Typography color="#ef5350" variant="caption">
                      ⚔️ {card.attack}
                    </Typography>
                    <Typography color="#66bb6a" variant="caption">
                      ❤️ {card.health}
                    </Typography>
                  </Stack>
                  <Typography
                    color="lightblue"
                    variant="caption"
                    sx={{ mt: 0.5, display: "block" }}
                  >
                    {card.text}
                  </Typography>
                </CardContent>
              </Card>
            </Grid2>
          ))}
        </Grid2>
      </Box>
    </Container>
  );
};

export default GameBoard;
