import React, { ReactNode } from "react";
import { Card } from "@/components/ui/card";

interface SectionProps {
  title: string;
  children: ReactNode;
}

export const Section: React.FC<SectionProps> = ({ title, children }) => {
  return (
    <div className="mb-8">
      <h2 className="text-xl font-semibold mb-3">{title}</h2>
      <Card className="border-border/40">
        {children}
      </Card>
    </div>
  );
};