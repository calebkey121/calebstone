import React from "react";
import { useGame } from "../../hooks/useGame";
import {
  Card,
  CardContent,
  Typography,
  Box,
  Stack,
  Tooltip,
  Zoom,
} from "@mui/material";

const GameCard = ({ card, index, isOpponent = false, type = "hand" }) => {
  const { selectedAttacker, selectAttacker, attack, playCard, gameState } =
    useGame();

  const handleClick = () => {
    if (type === "hand") {
      if (card.cost <= gameState.current_player.gold) {
        playCard(index);
      }
      return;
    }
    if (isOpponent && selectedAttacker !== null) {
      attack(selectedAttacker, index);
      return;
    }
    if (card.can_attack && !isOpponent) {
      selectAttacker(index);
    }
  };

  const isPlayable =
    type === "hand"
      ? card.cost <= gameState.current_player.gold
      : card.can_attack || (selectedAttacker !== null && isOpponent);

  const isSelected = type === "board" && selectedAttacker === index;

  return (
    <Tooltip
      title={card.text || ""}
      placement="top"
      TransitionComponent={Zoom}
      enterDelay={200}
      sx={{
        "& .MuiTooltip-tooltip": {
          bgcolor: "rgba(17, 24, 39, 0.95)",
          color: "rgb(125, 211, 252)",
          fontSize: "0.75rem",
          maxWidth: "none",
        },
      }}
    >
      <Card
        onClick={handleClick}
        sx={{
          position: "relative",
          backgroundColor: "rgba(255, 255, 255, 0.1)",
          backdropFilter: "blur(12px)",
          border: isSelected
            ? "2px solid rgb(96, 165, 250)"
            : "1px solid rgba(255, 255, 255, 0.2)",
          cursor: isPlayable ? "pointer" : "default",
          opacity: isPlayable ? 1 : 0.7,
          transition: "all 0.2s",
          "&:hover": {
            backgroundColor: "rgba(255, 255, 255, 0.15)",
            borderColor:
              isOpponent && selectedAttacker !== null
                ? "rgb(239, 68, 68)"
                : "rgb(96, 165, 250)",
          },
        }}
      >
        <CardContent>
          <Stack sx={{ justifyContent: "space-between", height: "100%" }}>
            <Typography
              variant="subtitle2"
              sx={{
                color: "white",
                fontWeight: 500,
                overflow: "hidden",
                textOverflow: "ellipsis",
                textAlign: "center",
              }}
            >
              {card.name}
            </Typography>

            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                gap: 1,
              }}
            >
              <Typography
                variant="caption"
                sx={{
                  color: "rgb(248, 113, 113)",
                  flex: 1,
                  textAlign: "center",
                }}
              >
                ⚔️ {card.attack}
              </Typography>
              <Typography
                variant="caption"
                sx={{
                  color: "rgb(234, 179, 8)",
                  flex: 1,
                  textAlign: "center",
                }}
              >
                💰 {card.cost}
              </Typography>
              <Typography
                variant="caption"
                sx={{
                  color: "rgb(74, 222, 128)",
                  flex: 1,
                  textAlign: "center",
                }}
              >
                ❤️ {card.health}
              </Typography>
            </Box>
          </Stack>
        </CardContent>
      </Card>
    </Tooltip>
  );
};

export default GameCard;
