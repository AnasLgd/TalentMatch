
import { useEffect } from "react";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { initializeTheme } from "@/lib/themes";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Consultants from "./pages/Consultants";
import Tenders from "./pages/Tenders";
import Matches from "./pages/Matches";
import Partners from "./pages/Partners";
import CvAnalysis from "./pages/CvAnalysis";
import DashboardLayout from "./components/layout/DashboardLayout";
import StyleGuide from "./pages/StyleGuide";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => {
  // Initialiser le thème au chargement de l'application
  useEffect(() => {
    initializeTheme();
  }, []);

  return (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<DashboardLayout />}>
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="consultants" element={<Consultants />} />
            <Route path="tenders" element={<Tenders />} />
            <Route path="matches" element={<Matches />} />
            <Route path="partners" element={<Partners />} />
            <Route path="cv-analysis" element={<CvAnalysis />} />
            <Route path="style-guide" element={<StyleGuide />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
  );
};

export default App;
