import React from "react";
import { Card, CardContent, Box, Typography } from "@mui/material";

const BoardContainer = ({ title, children }) => {
  return (
    <Card
      className="mb-4 min-h-[200px] relative"
      sx={{
        backgroundColor: "rgba(255, 255, 255, 0.05)",
        backdropFilter: "blur(8px)",
        border: "1px solid rgba(255, 255, 255, 0.2)",
        borderRadius: 2,
        position: "relative",
      }}
    >
      <Box
        sx={{
          background:
            "linear-gradient(135deg, rgb(88, 28, 135), rgb(30, 58, 138))",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          padding: "8px",
        }}
      >
        <Typography variant="caption" className="text-white/60">
          {title}
        </Typography>
      </Box>

      <CardContent className="p-4">{children}</CardContent>
    </Card>
  );
};

export default BoardContainer;
