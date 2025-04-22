import React, { useState, useMemo } from "react";
import { ArrowUpDown, MoreVertical, Edit, Trash2, FileText, Download } from "lucide-react";
import { ConsultantDisplay } from "@/features/consultants/types";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { PaginationControls } from "./PaginationControls";

// Constante pour le nombre d'éléments par page
const ITEMS_PER_PAGE = 5;

// Fonction utilitaire pour déterminer la couleur du badge de statut
const getStatusColor = (status: string): string => {
  switch (status) {
    case "Disponible":
      return "bg-green-100 text-green-800";
    case "Qualifié":
      return "bg-purple-100 text-purple-800";
    case "En cours de process":
      return "bg-blue-100 text-blue-800";
    case "En mission":
      return "bg-amber-100 text-amber-800";
    case "Intercontrat":
      return "bg-teal-100 text-teal-800";
    case "Indisponible":
      return "bg-red-100 text-red-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

interface ConsultantTableProps {
  consultants: ConsultantDisplay[];
}

export const ConsultantTable: React.FC<ConsultantTableProps> = ({ consultants }) => {
  // État pour gérer la pagination
  const [currentPage, setCurrentPage] = useState(0);
  
  // Calculer le nombre total de pages
  const totalPages = Math.ceil(consultants.length / ITEMS_PER_PAGE);
  
  // Obtenir les consultants pour la page actuelle
  const currentConsultants = useMemo(() => {
    const startIndex = currentPage * ITEMS_PER_PAGE;
    return consultants.slice(startIndex, startIndex + ITEMS_PER_PAGE);
  }, [consultants, currentPage]);
  
  // Gérer le changement de page
  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  if (consultants.length === 0) {
    return (
      <div className="p-8 text-center text-muted-foreground">
        Aucun consultant dans cette catégorie
      </div>
    );
  }

  // Déterminer si une hauteur fixe est nécessaire (uniquement si > 5 éléments)
  const needsFixedHeight = consultants.length > ITEMS_PER_PAGE;

  return (
    <div className="flex flex-col h-full">
      <div className={`relative w-full overflow-auto ${needsFixedHeight ? "flex-1" : ""}`}>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[300px]">
                <div className="flex items-center">
                  Nom
                  <ArrowUpDown className="ml-1 h-3 w-3" />
                </div>
              </TableHead>
              <TableHead>
                <div className="flex items-center">
                  Rôle
                  <ArrowUpDown className="ml-1 h-3 w-3" />
                </div>
              </TableHead>
              <TableHead>Expérience</TableHead>
              <TableHead>Compétences</TableHead>
              <TableHead>Statut</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentConsultants.map((consultant) => (
              <TableRow key={consultant.id}>
                <TableCell className="font-medium">
                  <div className="flex items-center gap-2">
                    <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center">
                      <span className="text-xs">
                        {consultant.name.split(" ").map(n => n[0]).join("")}
                      </span>
                    </div>
                    <span>{consultant.name}</span>
                  </div>
                </TableCell>
                <TableCell>{consultant.role}</TableCell>
                <TableCell>{consultant.experience}</TableCell>
                <TableCell>
                  <div className="flex flex-wrap gap-1">
                    {consultant.skills.map((skill, idx) => (
                      <Badge key={idx} variant="secondary">{skill.name}</Badge>
                    ))}
                  </div>
                </TableCell>
                <TableCell>
                  <span className={`inline-flex rounded-full px-2 py-1 text-xs ${getStatusColor(consultant.status)}`}>
                    {consultant.status}
                  </span>
                </TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon">
                        <MoreVertical className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>
                        <FileText className="mr-2 h-4 w-4" />
                        <span>Voir profil</span>
                      </DropdownMenuItem>
                      <DropdownMenuItem>
                        <Edit className="mr-2 h-4 w-4" />
                        <span>Modifier</span>
                      </DropdownMenuItem>
                      <DropdownMenuItem>
                        <Download className="mr-2 h-4 w-4" />
                        <span>Exporter CV</span>
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="text-red-500">
                        <Trash2 className="mr-2 h-4 w-4" />
                        <span>Supprimer</span>
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      
      {/* Contrôles de pagination - affichés seulement s'il y a plus d'une page */}
      {totalPages > 1 && (
        <PaginationControls
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={handlePageChange}
        />
      )}
    </div>
  );
};