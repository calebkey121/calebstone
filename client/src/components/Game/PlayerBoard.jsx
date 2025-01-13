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
  return (
    <Box>
      <Army player={player} />
      <PlayerStats player={player} isOpponent={false} />
      <Hand current_player={player} />
    </Box>
  );
};

export default PlayerBoard;
