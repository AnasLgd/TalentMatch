
import React, { useContext } from "react";
import { NavLink } from "react-router-dom";
import {
  BarChart3,
  Users,
  Briefcase,
  Search,
  Settings,
  LogOut,
  UserPlus,
  FileText,
  ChevronLeft,
  ChevronRight
} from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { DashboardContext } from "./DashboardLayout";
import { cn } from "@/lib/utils";

interface SidebarProps {
  expanded?: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ expanded = true }) => {
  const { toggleSidebar } = useContext(DashboardContext);
  
  const menuItems = [
    { name: "Tableau de bord", icon: BarChart3, path: "/dashboard" },
    { name: "Consultants", icon: Users, path: "/consultants" },
    { name: "Appels d'offres", icon: Briefcase, path: "/tenders" },
    { name: "Matching", icon: Search, path: "/matches" },
    { name: "ESN Partenaires", icon: UserPlus, path: "/partners" },
    { name: "CV & Analyse", icon: FileText, path: "/cv-analysis" }
  ];

  return (
    <aside
      className={cn(
        "fixed top-0 bottom-0 left-0 flex flex-col bg-white border border-gray-200 transition-all duration-300 z-40 overflow-hidden",
        "p-4 m-3 rounded-2xl shadow-sm",
        expanded ? "lg:w-64" : "lg:w-20",
        "lg:translate-x-0",
        !expanded && "lg:items-center"
      )}
    >
      <div className={cn(
        "flex items-center py-4 px-2",
        !expanded && "justify-center"
      )}>
        <span className="bg-primary rounded-xl p-2 shadow-sm border border-primary/10">
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
        {expanded && <h1 className="text-xl font-semibold ml-2">TalentMatch</h1>}
        
        {/* Toggle button */}
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleSidebar}
          className={cn(
            "rounded-full ml-auto p-1 text-muted-foreground hover:bg-muted shadow-sm transition-all",
            !expanded && "hidden"
          )}
        >
          <ChevronLeft className="h-5 w-5" />
        </Button>
        
        {/* Expand button */}
        {!expanded && (
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleSidebar}
            className="rounded-full mt-4 p-1 text-muted-foreground hover:bg-muted shadow-sm transition-all"
          >
            <ChevronRight className="h-5 w-5" />
          </Button>
        )}
      </div>

      <nav className="flex-1 overflow-y-auto py-6">
        <ul className={cn(
          "space-y-3",
          expanded ? "px-2" : "px-0"
        )}>
          {menuItems.map((item) => (
            <li key={item.name}>
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-3 rounded-xl px-3 py-2.5 transition-all duration-200",
                    "hover:bg-emerald-50 hover:text-emerald-700 border border-transparent hover:border-emerald-100",
                    expanded ? "justify-start" : "justify-center",
                    isActive
                      ? "bg-emerald-50 text-emerald-700 font-medium border-emerald-100 shadow-inner"
                      : "text-muted-foreground"
                  )
                }
                title={!expanded ? item.name : undefined}
              >
                <item.icon className="h-5 w-5" />
                {expanded && <span>{item.name}</span>}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className={cn(
        "pt-4 space-y-4",
        expanded ? "px-2" : "px-0"
      )}>
        <Separator className="bg-border/30" />
        <div className={cn(
          "flex items-center",
          expanded ? "space-x-3" : "justify-center"
        )}>
          <div className="w-9 h-9 rounded-full bg-secondary/20 flex items-center justify-center border border-gray-200 shadow-sm">
            <span className="font-medium text-sm">JD</span>
          </div>
          {expanded && (
            <div>
              <p className="text-sm font-medium">John Doe</p>
              <p className="text-xs text-muted-foreground">Admin</p>
            </div>
          )}
        </div>
        {expanded && (
          <div className="space-y-2">
            <NavLink
              to="/settings"
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 rounded-xl px-3 py-2.5 transition-all duration-200",
                  "hover:bg-emerald-50 hover:text-emerald-700 border border-transparent hover:border-emerald-100",
                  isActive
                    ? "bg-emerald-50 text-emerald-700 font-medium border-emerald-100"
                    : "text-muted-foreground"
                )
              }
            >
              <Settings className="h-5 w-5" />
              <span>Paramètres</span>
            </NavLink>
            <NavLink
              to="/logout"
              className={cn(
                "flex items-center gap-3 rounded-xl px-3 py-2.5 transition-all duration-200",
                "hover:bg-emerald-50 hover:text-emerald-700 border border-transparent hover:border-emerald-100 text-muted-foreground"
              )}
            >
              <LogOut className="h-5 w-5" />
              <span>Se déconnecter</span>
            </NavLink>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
