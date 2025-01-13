import GameCard from "./GameCard";

const CardGrid = ({ cards, type = "hand", isOpponent = false }) => (
  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-2">
    {cards.map((card, index) => (
      <GameCard
        key={index}
        card={card}
        index={index}
        type={type}
        isOpponent={isOpponent}
      />
    ))}
  </div>
);

export default CardGrid;
