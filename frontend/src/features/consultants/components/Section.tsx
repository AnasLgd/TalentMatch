import React, { ReactNode } from "react";
import { Card } from "@/components/ui/card";

interface SectionProps {
  title: string;
  count: number;
  children: ReactNode;
  className?: string;
}

export const Section: React.FC<SectionProps> = ({ title, count, children, className = "" }) => {
  return (
    <div className={`h-full ${className}`}>
      <h2 className="text-xl font-semibold mb-3">
        {title} <span className="text-muted-foreground">({count})</span>
      </h2>
      <Card className="border-border/40 h-[calc(100%-2.5rem)]">
        {children}
      </Card>
    </div>
  );
};