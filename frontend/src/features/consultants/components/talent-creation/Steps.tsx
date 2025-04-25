import React, { ReactNode } from "react";
import { cva } from "class-variance-authority";
import { cn } from "@/lib/utils";
import { CheckIcon } from "lucide-react";

interface StepsProps {
  currentStep: number;
  totalSteps: number;
  children: ReactNode;
  className?: string;
}

interface StepProps {
  title: string;
  description?: string;
  isActive: boolean;
  isCompleted: boolean;
}

const stepVariants = cva(
  "flex items-center gap-2 p-2 rounded-lg transition-all relative",
  {
    variants: {
      state: {
        inactive: "text-muted-foreground",
        active: "text-primary bg-primary/10",
        completed: "text-primary",
      },
    },
    defaultVariants: {
      state: "inactive",
    },
  }
);

export const Step: React.FC<StepProps> = ({
  title,
  description,
  isActive,
  isCompleted,
}) => {
  return (
    <div
      className={cn(
        stepVariants({
          state: isActive ? "active" : isCompleted ? "completed" : "inactive",
        }),
        "flex-1"
      )}
    >
      <div className="flex items-center">
        <div
          className={cn(
            "w-8 h-8 rounded-full flex items-center justify-center mr-2",
            isActive
              ? "bg-primary text-primary-foreground"
              : isCompleted
              ? "bg-primary text-primary-foreground"
              : "bg-muted text-muted-foreground"
          )}
        >
          {isCompleted ? <CheckIcon className="h-4 w-4" /> : null}
          {!isCompleted && <span className="text-sm font-medium">•</span>}
        </div>
        <div>
          <div className="font-medium">{title}</div>
          {description && (
            <div className="text-xs text-muted-foreground">{description}</div>
          )}
        </div>
      </div>
    </div>
  );
};

export const Steps: React.FC<StepsProps> = ({
  currentStep,
  totalSteps,
  children,
  className,
}) => {
  return (
    <div className={cn("mx-auto px-4 py-2", className)}>
      <div className="flex overflow-x-auto gap-2 md:gap-4">
        {children}
      </div>
      <div className="mt-2 flex justify-between text-sm text-muted-foreground">
        <div>
          Étape {currentStep + 1} sur {totalSteps}
        </div>
        <div className="font-medium">
          {Math.round(((currentStep + 1) / totalSteps) * 100)}%
        </div>
      </div>
    </div>
  );
};