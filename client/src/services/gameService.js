// src/services/gameService.js
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

const gameService = {
  async startNewGame() {
    const { data } = await axios.post(`${API_URL}/new_game`);
    // debugger;
    return data;
  },

  async getGameState(sessionId) {
    const { data } = await axios.get(`${API_URL}/game_state/${sessionId}`);
    return data;
  },

  async sendAction(sessionId, action) {
    const { data } = await axios.post(`${API_URL}/action/${sessionId}`, action);
    return data;
  },
};

export default gameService;
