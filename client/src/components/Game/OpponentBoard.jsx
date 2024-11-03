import React from "react";
import { Box, Typography, Grid2 } from "@mui/material";
import PlayerStats from "./PlayerStats";
import Army from "./Army";

const OpponentBoard = ({ player }) => {
  return (
    <>
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={2}
      >
        <PlayerStats player={player} isOpponent={true} />
        <Typography color="rgba(255,255,255,0.6)">
          Cards in hand: {player.hand.length}
        </Typography>
      </Box>
      <Army player={player} />
    </>
  );
};

export default OpponentBoard;
