import React, { useState, useEffect } from "react";
import cardService from "../../services/cardService";
import { Loader2 } from "lucide-react";

const CardCollection = () => {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortKey, setSortKey] = useState("cost");
  const [filterText, setFilterText] = useState("");

  useEffect(() => {
    const fetchCards = async () => {
      try {
        const cardsData = await cardService.getAllCards();
        // Convert object to array for easier sorting/filtering
        const cardsArray = Object.entries(cardsData).map(([key, card]) => ({
          id: key,
          ...card,
        }));
        setCards(cardsArray);
      } catch (err) {
        setError("Failed to load cards");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCards();
  }, []);

  const sortedAndFilteredCards = React.useMemo(() => {
    return cards
      .filter(
        (card) =>
          card.name.toLowerCase().includes(filterText.toLowerCase()) ||
          card.effect_text.toLowerCase().includes(filterText.toLowerCase())
      )
      .sort((a, b) => {
        if (sortKey === "name") {
          return a.name.localeCompare(b.name);
        }
        return a[sortKey] - b[sortKey];
      });
  }, [cards, sortKey, filterText]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 text-white animate-spin" />
      </div>
    );
  }

  if (error) {
    return <div className="text-center text-red-500 p-4">{error}</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Controls */}
      <div className="mb-6 flex flex-col sm:flex-row gap-4 items-center justify-between">
        <input
          type="text"
          placeholder="Search cards..."
          className="px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:border-white/40"
          value={filterText}
          onChange={(e) => setFilterText(e.target.value)}
        />

        <select
          value={sortKey}
          onChange={(e) => setSortKey(e.target.value)}
          className="px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:border-white/40"
        >
          <option value="cost">Sort by Cost</option>
          <option value="name">Sort by Name</option>
          <option value="attack_value">Sort by Attack</option>
          <option value="health">Sort by Health</option>
        </select>
      </div>

      {/* Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sortedAndFilteredCards.map((card) => (
          <div
            key={card.id}
            className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 hover:border-white/40 transition-colors"
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-bold text-white">{card.name}</h3>
              <span className="px-3 py-1 bg-white/20 rounded-full text-sm text-white">
                {card.cost} 💵
              </span>
            </div>

            <div className="flex gap-4 mb-4">
              <div className="flex items-center gap-2">
                <span className="text-red-400">⚔️ {card.attack_value}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-green-400">❤️ {card.health}</span>
              </div>
            </div>

            <p className="text-blue-200 text-sm">{card.effect_text}</p>
          </div>
        ))}
      </div>

      {/* Card Count */}
      <div className="mt-6 text-center text-white/60">
        Showing {sortedAndFilteredCards.length} of {cards.length} cards
      </div>
    </div>
  );
};

export default CardCollection;
