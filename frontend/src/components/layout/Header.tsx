import React, { useState } from "react";
import {
  Bell,
  Search,
  Menu,
  MessageSquare,
  User,
  BarChart3,
  Users,
  Briefcase,
  UserPlus,
  FileText,
  Settings,
  LogOut
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import ThemeSwitcher from "@/components/ui/theme-switcher";
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuLabel, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { NavLink } from "react-router-dom";

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);
  
  const menuItems = [
    { name: "Tableau de bord", icon: BarChart3, path: "/dashboard" },
    { name: "Consultants", icon: Users, path: "/consultants" },
    { name: "Appels d'offres", icon: Briefcase, path: "/tenders" },
    { name: "Matching", icon: Search, path: "/matches" },
    { name: "ESN Partenaires", icon: UserPlus, path: "/partners" },
    { name: "CV & Analyse", icon: FileText, path: "/cv-analysis" }
  ];

  return (
    <header className="h-16 w-full flex items-center justify-between rounded-2xl bg-white shadow-sm border border-gray-200 px-6">
      <div className="flex items-center lg:hidden">
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="shadow-sm rounded-xl hover:shadow-md transition-all">
              <Menu className="h-5 w-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-[250px] p-0">
            <div className="flex flex-col h-full bg-card">
              <div className="p-6 border-b border-border/40">
                <div className="flex items-center">
                  <span className="bg-primary rounded-lg p-2">
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
                          `flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:bg-accent hover:text-accent-foreground ${
                            isActive
                              ? "bg-accent text-accent-foreground font-medium"
                              : "text-muted-foreground"
                          }`
                        }
                        onClick={() => setIsOpen(false)}
                      >
                        <item.icon className="h-4 w-4" />
                        <span>{item.name}</span>
                      </NavLink>
                    </li>
                  ))}
                </ul>
              </nav>

              <div className="p-4 border-t border-border/40">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-9 h-9 rounded-full bg-muted flex items-center justify-center">
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
                      `flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:bg-accent hover:text-accent-foreground ${
                        isActive
                          ? "bg-accent text-accent-foreground font-medium"
                          : "text-muted-foreground"
                      }`
                    }
                    onClick={() => setIsOpen(false)}
                  >
                    <Settings className="h-4 w-4" />
                    <span>Paramètres</span>
                  </NavLink>
                  <NavLink
                    to="/logout"
                    className="flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:bg-accent hover:text-accent-foreground text-muted-foreground"
                    onClick={() => setIsOpen(false)}
                  >
                    <LogOut className="h-4 w-4" />
                    <span>Se déconnecter</span>
                  </NavLink>
                </div>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </div>

      <div className="hidden md:flex max-w-md w-full">
        <div className="relative w-full max-w-md">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Rechercher..."
            className="pl-10 bg-white/90 rounded-xl shadow-inner border border-gray-200"
          />
        </div>
      </div>
      <div className="flex items-center space-x-3">
        <ThemeSwitcher />
        
        <div className="flex items-center space-x-2 pr-2">
          <Button variant="ghost" size="icon" className="relative shadow-sm rounded-xl hover:shadow-md transition-all bg-white">
            <MessageSquare className="h-5 w-5" />
            <span className="absolute top-1 right-1 h-2 w-2 bg-primary rounded-full"></span>
          </Button>
          
          <Button variant="ghost" size="icon" className="relative shadow-sm rounded-xl hover:shadow-md transition-all bg-white">
            <Bell className="h-5 w-5" />
            <span className="absolute top-1 right-1 h-2 w-2 bg-primary rounded-full"></span>
          </Button>
          
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="rounded-xl shadow-sm hover:shadow-md transition-all bg-white">
                <User className="h-5 w-5" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Mon compte</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Profil</DropdownMenuItem>
              <DropdownMenuItem>Paramètres</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Se déconnecter</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
};

export default Header;
