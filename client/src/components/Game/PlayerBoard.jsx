import React from "react";
import { useGame } from "../../hooks/useGame";
import { Box, Typography, Grid2, Button, Stack } from "@mui/material";
import {
  SyncAlt as EndTurnIcon,
  Cancel as CancelIcon,
} from "@mui/icons-material";
import PlayerStats from "./PlayerStats";
import Hand from "./Hand";
import Army from "./Army";

const PlayerBoard = ({ player }) => {
  const { endTurn, selectedAttacker, cancelAttack } = useGame();
  return (
    <Box>
      <Army player={player} />
      <PlayerStats player={player} isOpponent={false} />
      <Hand current_player={player} />
      <Box display="flex" justifyContent="space-between" alignItems="center">
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
    </Box>
  );
};

export default PlayerBoard;
