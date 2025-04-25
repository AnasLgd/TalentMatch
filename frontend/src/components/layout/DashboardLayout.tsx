
import React, { useState, useEffect } from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Header from "./Header";
import { Toaster } from "@/components/ui/toaster";
import { Menu } from "lucide-react";
import { Button } from "@/components/ui/button";

// Create a DashboardContext to share sidebar state with child components
export const DashboardContext = React.createContext({
  sidebarExpanded: true,
  toggleSidebar: () => {},
});

const DashboardLayout = () => {
  const [sidebarExpanded, setSidebarExpanded] = useState(true);
  
  // Toggle sidebar function
  const toggleSidebar = () => {
    setSidebarExpanded(prev => !prev);
  };

  // Provide the context values
  const contextValue = {
    sidebarExpanded,
    toggleSidebar,
  };

  return (
    <DashboardContext.Provider value={contextValue}>
      <div className="min-h-screen bg-gray-50 flex overflow-hidden relative">
        {/* Sidebar with conditional classes for expanded/collapsed state */}
        <Sidebar expanded={sidebarExpanded} />
        
        {/* Main content area - adapts its left margin based on sidebar state */}
        <div className={`flex-1 flex flex-col overflow-hidden transition-all duration-300 ${
          sidebarExpanded ? 'lg:ml-64' : 'lg:ml-20'
        }`}>
          {/* Fixed header with neumorphism styling - width adapts to sidebar state with consistent margins */}
          <div className={`fixed top-0 z-40 transition-all duration-300 p-3 ${
            sidebarExpanded ? 'lg:left-[calc(16rem+24px)]' : 'lg:left-[calc(5rem+24px)]'
          } right-3`}>
            <Header />
          </div>
          
          {/* Mobile sidebar toggle button - visible only on small screens */}
          <div className="lg:hidden fixed left-4 top-4 z-50">
            <Button
              variant="outline"
              size="icon"
              onClick={toggleSidebar}
              className="rounded-full neu-shadow-flat h-10 w-10 bg-white border border-gray-200"
            >
              <Menu className="h-5 w-5" />
            </Button>
          </div>
          
          {/* Main content with padding to account for fixed header and footer */}
          <main className="flex-1 overflow-y-auto p-6 pt-24 pb-32">
            <Outlet />
          </main>
          
          {/* Fixed footer container - width adapts to sidebar state with consistent margins */}
          <div className={`fixed bottom-0 z-40 transition-all duration-300 p-3 ${
            sidebarExpanded ? 'lg:left-[calc(16rem+24px)]' : 'lg:left-[calc(5rem+24px)]'
          } right-3`}>
            {/* Footer content will be provided by page components when needed */}
          </div>
        </div>
        <Toaster />
      </div>
    </DashboardContext.Provider>
  );
};

export default DashboardLayout;
