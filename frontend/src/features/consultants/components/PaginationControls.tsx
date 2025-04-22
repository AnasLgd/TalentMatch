import React from "react";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface PaginationControlsProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export const PaginationControls: React.FC<PaginationControlsProps> = ({
  currentPage,
  totalPages,
  onPageChange,
}) => {
  // Si totalPages <= 1, ne pas afficher les contrôles
  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-end py-2 px-4 border-t border-gray-200">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 0}
        className="text-xs"
      >
        <ChevronLeft className="h-4 w-4 mr-1" />
        Précédent
      </Button>
      <span className="mx-4 text-sm">
        Page {currentPage + 1} sur {totalPages}
      </span>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages - 1}
        className="text-xs"
      >
        Suivant
        <ChevronRight className="h-4 w-4 ml-1" />
      </Button>
    </div>
  );
};