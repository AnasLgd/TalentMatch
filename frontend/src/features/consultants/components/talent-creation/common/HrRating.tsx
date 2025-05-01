import React from "react";
import { Star } from "lucide-react";
import { cn } from "@/lib/utils";

interface HrRatingProps {
  value: number;
  onChange?: (value: number) => void;
  size?: "sm" | "md" | "lg";
  readOnly?: boolean;
}

export const HrRating: React.FC<HrRatingProps> = ({
  value,
  onChange = () => {},
  size = "md",
  readOnly = false,
}) => {
  const stars = [1, 2, 3, 4, 5];
  
  const getStarSize = () => {
    switch (size) {
      case "sm":
        return "h-4 w-4";
      case "lg":
        return "h-6 w-6";
      default:
        return "h-5 w-5";
    }
  };
  
  return (
    <div className="flex items-center space-x-1" role="group" aria-label="Notation sur 5 étoiles">
      {stars.map((star) => (
        <button
          key={star}
          type="button"
          onClick={() => !readOnly && onChange(star)}
          className={cn(
            "rounded-sm transition-colors duration-150",
            !readOnly && "focus:outline-none focus-visible:ring-2 focus-visible:ring-primary",
            star <= value ? "text-yellow-500" : "text-muted",
            readOnly ? "cursor-default pointer-events-none" : "hover:text-yellow-400"
          )}
          aria-label={`${star} étoile${star > 1 ? 's' : ''}`}
          aria-pressed={star <= value}
          disabled={readOnly}
        >
          <Star
            className={cn(
              getStarSize(),
              star <= value ? "fill-yellow-500" : "fill-none",
              !readOnly && star > value && "hover:fill-yellow-100"
            )}
          />
        </button>
      ))}
    </div>
  );
};