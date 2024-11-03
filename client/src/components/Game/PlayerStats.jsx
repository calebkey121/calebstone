import { Card, CardContent, Typography, Stack } from "@mui/material";

const PlayerStats = ({ player, isOpponent = false }) => (
  <Stack direction="row" spacing={2} alignItems="center">
    <Card
      sx={{
        bgcolor: "rgba(255, 255, 255, 0.1)",
        backdropFilter: "blur(10px)",
      }}
    >
      <CardContent sx={{ p: 2, "&:last-child": { pb: 2 } }}>
        <Typography color="white" fontWeight="bold">
          {isOpponent ? "Opponent" : "You"}
        </Typography>
        <Typography variant="body2" color="lightblue">
          ❤️ {player.hero.health}
        </Typography>
      </CardContent>
    </Card>
    <Card
      sx={{
        bgcolor: "rgba(255, 255, 255, 0.1)",
        backdropFilter: "blur(10px)",
      }}
    >
      <CardContent sx={{ p: 2, "&:last-child": { pb: 2 } }}>
        <Typography variant="body2" color="gold">
          💰 {player.gold} Gold
        </Typography>
        <Typography variant="body2" color="lightgreen">
          📈 {player.income} Income
        </Typography>
      </CardContent>
    </Card>
  </Stack>
);

export default PlayerStats;
