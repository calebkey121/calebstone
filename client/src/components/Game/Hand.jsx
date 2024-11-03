import React from "react";
import GameCard from "./GameCard";
import { Grid2 } from "@mui/material";
const Hand = ({ current_player }) => {
  return (
    <Grid2 container spacing={1}>
      {current_player.hand.map((card, index) => (
        <Grid2 item xs={1.5} key={index}>
          <GameCard card={card} index={index} type="hand" />
        </Grid2>
      ))}
    </Grid2>
  );
};

export default Hand;
