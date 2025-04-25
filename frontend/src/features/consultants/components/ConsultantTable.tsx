import React, { useState, useMemo } from "react";
import { ArrowUpDown, MoreVertical, Edit, Trash2, FileText, Download, Plus } from "lucide-react";
import { ConsultantDisplay, Skill } from "@/features/consultants/types";
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
import { Tooltip } from "@/components/ui/tooltip";

// Constante pour le nombre d'éléments par page
const ITEMS_PER_PAGE = 5;
// Constante pour le nombre maximum de compétences à afficher
const MAX_SKILLS_DISPLAYED = 5;

// Fonction utilitaire pour déterminer la couleur et le tooltip du badge de statut
const getStatusInfo = (status: string, availabilityDate?: string): { color: string, tooltip?: string } => {
  // Vérifier si la date est future ou passée/aujourd'hui
  const isDateInFuture = () => {
    if (!availabilityDate) return false;
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Réinitialiser à minuit pour comparer les dates
    const availDate = new Date(availabilityDate);
    return availDate > today;
  };

  // Formater la date pour l'affichage
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('fr-FR');
  };

  switch (status) {
    case "Disponible":
      return {
        color: "bg-green-100 text-green-800",
        tooltip: "Consultant qualifié et disponible immédiatement"
      };
    case "Qualifié":
      return {
        color: "bg-purple-100 text-purple-800",
        tooltip: "Consultant qualifié (statut de disponibilité non précisé)"
      };
    case "Qualifié - Disponible":
      return {
        color: "bg-green-100 text-green-800",
        tooltip: "Consultant qualifié et disponible immédiatement"
      };
    case "Bientôt disponible":
      return {
        color: "bg-sky-100 text-sky-800",
        tooltip: availabilityDate ? `Disponible à partir du ${formatDate(availabilityDate)}` : "Date de disponibilité future"
      };
    case "En cours de process":
    case "En création":
      return {
        color: "bg-blue-100 text-blue-800",
        tooltip: "Consultant en cours de création ou qualification"
      };
    case "En mission":
      return {
        color: "bg-amber-100 text-amber-800",
        tooltip: "Consultant actuellement en mission chez un client"
      };
    case "Intercontrat":
      return {
        color: "bg-teal-100 text-teal-800",
        tooltip: "Consultant en période d'intercontrat, disponible pour mission"
      };
    case "Archivé":
      return {
        color: "bg-gray-100 text-gray-800",
        tooltip: "Consultant archivé (n'est plus actif)"
      };
    default:
      return {
        color: "bg-gray-100 text-gray-800"
      };
  }
};

// Format du texte d'expérience (gestion singulier/pluriel)
const formatExperience = (experience: string): string => {
  const numericValue = parseInt(experience);
  if (isNaN(numericValue)) return experience;
  
  return numericValue === 1 ? "1 an" : `${numericValue} ans`;
};

// Composant pour afficher les compétences avec un badge +X si nécessaire
const SkillsList = ({ skills }: { skills: Skill[] }) => {
  if (skills.length <= MAX_SKILLS_DISPLAYED) {
    return (
      <div className="flex flex-wrap gap-1">
        {skills.map((skill, idx) => (
          <Badge key={idx} variant="secondary">{skill.name}</Badge>
        ))}
      </div>
    );
  }

  // Si plus de 5 compétences, on n'en affiche que 5 et on ajoute un badge +X
  const displayedSkills = skills.slice(0, MAX_SKILLS_DISPLAYED);
  const remainingCount = skills.length - MAX_SKILLS_DISPLAYED;
  
  return (
    <div className="flex flex-wrap gap-1">
      {displayedSkills.map((skill, idx) => (
        <Badge key={idx} variant="secondary">{skill.name}</Badge>
      ))}
      
      <Tooltip
        content={
          <div className="max-w-xs">
            <p className="font-semibold mb-1">Autres compétences :</p>
            <div className="flex flex-wrap gap-1">
              {skills.slice(MAX_SKILLS_DISPLAYED).map((skill, idx) => (
                <Badge key={idx} variant="secondary">{skill.name}</Badge>
              ))}
            </div>
          </div>
        }
      >
        <Badge variant="outline" className="cursor-help">
          <Plus className="h-3 w-3 mr-1" />
          {remainingCount}
        </Badge>
      </Tooltip>
    </div>
  );
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
              <TableHead className="w-[250px]">
                <div className="flex items-center">
                  Nom
                  <ArrowUpDown className="ml-1 h-3 w-3" />
                </div>
              </TableHead>
              <TableHead className="w-[200px]">
                <div className="flex items-center">
                  Rôle
                  <ArrowUpDown className="ml-1 h-3 w-3" />
                </div>
              </TableHead>
              <TableHead className="w-[100px]">Expérience</TableHead>
              <TableHead>Compétences</TableHead>
              <TableHead className="w-[140px]">Statut</TableHead>
              <TableHead className="text-right w-[80px]">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentConsultants.map((consultant) => (
              <TableRow key={consultant.id}>
                <TableCell className="font-medium">
                  <Tooltip content={consultant.name}>
                    <div className="flex items-center gap-2">
                      <div className="h-8 w-8 min-w-8 rounded-full bg-muted flex items-center justify-center">
                        <span className="text-xs">
                          {consultant.name.split(" ").map(n => n[0]).join("")}
                        </span>
                      </div>
                      <span className="truncate max-w-[180px]">{consultant.name}</span>
                    </div>
                  </Tooltip>
                </TableCell>
                <TableCell>
                  <Tooltip content={consultant.role}>
                    <div className="truncate max-w-[140px]">{consultant.role}</div>
                  </Tooltip>
                </TableCell>
                <TableCell>{formatExperience(consultant.experience)}</TableCell>
                <TableCell>
                  <SkillsList skills={consultant.skills} />
                </TableCell>
                <TableCell>
                  <div className="w-full flex justify-start">
                    {(() => {
                      const statusInfo = getStatusInfo(consultant.status, consultant.availabilityDate);
                      return (
                        <Tooltip content={statusInfo.tooltip || consultant.status}>
                          <span className={`inline-flex rounded-full px-3 py-1 text-xs min-w-24 justify-center ${statusInfo.color}`}>
                            {consultant.status}
                          </span>
                        </Tooltip>
                      );
                    })()}
                  </div>
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