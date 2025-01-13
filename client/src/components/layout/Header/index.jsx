// src/components/layout/Header/index.jsx
import React from "react";
import { useLocation, Link } from "react-router-dom";
import { Home } from "lucide-react";

const Header = () => {
  const location = useLocation();

  // Don't show header on main menu
  if (location.pathname === "/") {
    return null;
  }

  return (
    <header className="bg-white/10 backdrop-blur-sm border-b border-white/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <Link
              to="/"
              className="text-white hover:text-blue-200 transition-colors"
              title="Return to Main Menu"
            >
              <Home className="w-6 h-6" />
            </Link>
          </div>

          <h1 className="text-xl font-bold text-white">
            {location.pathname === "/play" && "Calebstone"}
            {location.pathname === "/cards" && "Card Collection"}
          </h1>

          <div className="w-6"> {/* Empty div for flex spacing */}</div>
        </div>
      </div>
    </header>
  );
};

export default Header;
