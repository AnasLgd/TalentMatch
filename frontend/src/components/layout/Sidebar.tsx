
import React from "react";
import { NavLink } from "react-router-dom";
import { 
  BarChart3, 
  Users, 
  Briefcase, 
  Search, 
  Settings, 
  LogOut, 
  UserPlus, 
  FileText
} from "lucide-react";
import { Separator } from "@/components/ui/separator";

const Sidebar = () => {
  const menuItems = [
    { name: "Tableau de bord", icon: BarChart3, path: "/dashboard" },
    { name: "Consultants", icon: Users, path: "/consultants" },
    { name: "Appels d'offres", icon: Briefcase, path: "/tenders" },
    { name: "Matching", icon: Search, path: "/matches" },
    { name: "ESN Partenaires", icon: UserPlus, path: "/partners" },
    { name: "CV & Analyse", icon: FileText, path: "/cv-analysis" }
  ];

  return (
    <aside className="hidden lg:flex h-screen w-64 flex-col bg-card border-r border-border/30 shadow-sm">
      <div className="p-6">
        <div className="flex items-center">
          <span className="bg-primary rounded-lg p-2 shadow-sm">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="20" 
              height="20" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              className="text-primary-foreground"
            >
              <path d="M17 18a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v9Z"></path>
              <path d="m12 12 4-4"></path>
              <path d="M8 8v4"></path>
              <path d="M8 12h4"></path>
            </svg>
          </span>
          <h1 className="text-xl font-bold ml-2">TalentMatch</h1>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto py-4">
        <ul className="px-3 space-y-1">
          {menuItems.map((item) => (
            <li key={item.name}>
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-lg px-3 py-2 transition-all duration-300 hover:bg-primary/10 hover:text-foreground ${
                    isActive
                      ? "bg-primary/15 text-primary font-medium"
                      : "text-muted-foreground"
                  }`
                }
              >
                <item.icon className="h-5 w-5" />
                <span>{item.name}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="p-6 space-y-4">
        <Separator />
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-full bg-secondary/20 flex items-center justify-center">
            <span className="font-medium text-sm">JD</span>
          </div>
          <div>
            <p className="text-sm font-medium">John Doe</p>
            <p className="text-xs text-muted-foreground">Admin</p>
          </div>
        </div>
        <div className="space-y-1">
          <NavLink
            to="/settings"
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 transition-all duration-300 hover:bg-primary/10 hover:text-foreground ${
                isActive
                  ? "bg-primary/15 text-primary font-medium"
                  : "text-muted-foreground"
              }`
            }
          >
            <Settings className="h-5 w-5" />
            <span>Paramètres</span>
          </NavLink>
          <NavLink
            to="/logout"
            className="flex items-center gap-3 rounded-lg px-3 py-2 transition-all duration-300 hover:bg-primary/10 hover:text-foreground text-muted-foreground"
          >
            <LogOut className="h-5 w-5" />
            <span>Se déconnecter</span>
          </NavLink>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
