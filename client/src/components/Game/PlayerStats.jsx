import { Card, CardContent, Typography, Stack } from "@mui/material";

const PlayerStats = ({ player, isOpponent = false }) => (
  <Card
    sx={{
      width: "100%",
      height: "100%",
      bgcolor: "rgba(255, 255, 255, 0.1)",
      backdropFilter: "blur(10px)",
    }}
  >
    <CardContent sx={{ p: 2, "&:last-child": { pb: 2 } }}>
      <Stack spacing={2} alignItems="center">
        <Typography color="white" fontWeight="bold" textAlign="center">
          {isOpponent ? "Opponent" : "You"}
        </Typography>
        <Typography variant="body2" color="lightblue" textAlign="center">
          ❤️ {player.hero.health}
        </Typography>
        <Typography variant="body2" color="gold" textAlign="center">
          💰 {player.gold}
        </Typography>
        <Typography variant="body2" color="lightgreen" textAlign="center">
          📈 {player.income}
        </Typography>
      </Stack>
    </CardContent>
  </Card>
);

export default PlayerStats;
