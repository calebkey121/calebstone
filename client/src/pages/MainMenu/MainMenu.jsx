import React from "react";
import { Menu, Github, Play, BookOpen } from "lucide-react";
import { useNavigate } from "react-router-dom";

const MainMenu = () => {
  const navigate = useNavigate();
  const menuItems = [
    {
      title: "Play Game",
      description: "Start a new game of Calebstone",
      icon: <Play className="w-6 h-6" />,
      onClick: () => navigate("/play"),
    },
    {
      title: "Card Collection",
      description: "Browse all available cards",
      icon: <BookOpen className="w-6 h-6" />,
      onClick: () => navigate("/cards"),
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-blue-900 flex flex-col items-center justify-center p-4">
      {/* Logo Section */}
      <div className="mb-8 text-center">
        <h1 className="text-6xl font-bold text-white mb-2 tracking-tight">
          Calebstone
        </h1>
        <p className="text-blue-200 text-xl">Welcome to the battlefield</p>
      </div>

      {/* Menu Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl w-full">
        {menuItems.map((item, index) => (
          <button
            key={index}
            onClick={item.onClick}
            className="group bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-300 rounded-lg p-6 flex items-center space-x-4 border border-white/20 hover:border-white/40"
          >
            <div className="rounded-full bg-white/10 p-3 group-hover:bg-white/20 transition-colors">
              {item.icon}
            </div>
            <div className="text-left">
              <h2 className="text-xl font-semibold text-white mb-1">
                {item.title}
              </h2>
              <p className="text-blue-200 text-sm">{item.description}</p>
            </div>
          </button>
        ))}
      </div>

      {/* Footer */}
      <div className="mt-12 text-center text-blue-200">
        <p className="text-sm mb-2">Version 0.0.1</p>
        <a
          href="https://github.com/calebkey121/Calebstone"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center space-x-2 text-sm hover:text-white transition-colors"
        >
          <Github className="w-4 h-4" />
          <span>View on GitHub</span>
        </a>
      </div>
    </div>
  );
};

export default MainMenu;
