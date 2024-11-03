import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

const cardService = {
  async getAllCards() {
    const { data } = await axios.get(`${API_URL}/cards`);
    return data;
  },
};

export default cardService;
