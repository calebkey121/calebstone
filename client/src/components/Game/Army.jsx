import React from "react";
import { Grid2 } from "@mui/material";
import GameCard from "./GameCard";

const Army = ({ player }) => (
  <Grid2 container spacing={1}>
    {player.army.map((ally, index) => (
      <Grid2 item xs={1.5} key={index}>
        <GameCard card={ally} index={index} type="board" isOpponent={false} />
      </Grid2>
    ))}
  </Grid2>
);

export default Army;
