import React, { useState, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import {
  Search,
  Plus, 
  Filter, 
  ArrowUpDown,
  MoreVertical,
  Edit,
  Trash2,
  FileText,
  Download,
  Upload
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { CreateConsultantModal } from "@/features/consultants/components/CreateConsultantModal";
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { useConsultants } from "@/features/consultants/hooks/useConsultants";
import { ConsultantDisplay } from "@/features/consultants/types";

// Fonction utilitaire pour déterminer la couleur du badge de statut
const getStatusColor = (status: string): string => {
  switch (status) {
    case "Disponible":
      return "bg-green-100 text-green-800";
    case "Partiellement disponible":
      return "bg-blue-100 text-blue-800";
    case "En mission":
      return "bg-amber-100 text-amber-800";
    case "Indisponible":
      return "bg-red-100 text-red-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

const Consultants = () => {
  const navigate = useNavigate();
  const {
    consultants,
    isLoading,
    isError,
    error,
  } = useConsultants();

  const [searchTerm, setSearchTerm] = useState("");
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  // Filtrer les consultants directement dans le rendu plutôt que dans un effet
  const filteredConsultants = useMemo(() => {
    if (!consultants || searchTerm.trim() === "") {
      return consultants || [];
    } else {
      const term = searchTerm.toLowerCase();
      return consultants.filter(
        (consultant) =>
          consultant.name.toLowerCase().includes(term) ||
          consultant.role.toLowerCase().includes(term) ||
          consultant.skills.some((skill) => skill.name.toLowerCase().includes(term))
      );
    }
  }, [consultants, searchTerm]);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Consultants</h1>
        <p className="text-muted-foreground">
          Gérez vos consultants, leurs compétences et disponibilités.
        </p>
      </div>

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative max-w-md w-full">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Rechercher par nom, compétence..."
            className="pl-10"
            value={searchTerm}
            onChange={handleSearch}
          />
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon">
            <Filter className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            onClick={() => navigate('/cv-analysis')}
          >
            <Upload className="mr-2 h-4 w-4" />
            Importer CV
          </Button>
          <Button onClick={() => setIsCreateModalOpen(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Ajouter un consultant
          </Button>
        </div>
      </div>

      {isLoading && (
        <div className="w-full p-8 text-center">
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded-md mb-4 w-3/4 mx-auto"></div>
            <div className="h-4 bg-gray-200 rounded-md mb-4 w-1/2 mx-auto"></div>
            <div className="h-4 bg-gray-200 rounded-md w-2/3 mx-auto"></div>
          </div>
          <p className="mt-4 text-muted-foreground">Chargement des consultants...</p>
        </div>
      )}
      
      {isError && (
        <div className="w-full p-8 text-center">
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-red-600 font-medium">Une erreur est survenue lors du chargement des consultants</p>
            <p className="text-red-500 text-sm mt-1">{String(error)}</p>
          </div>
        </div>
      )}
      
      {!isLoading && !isError && (
        <Card className="border-border/40">
          <div className="relative w-full overflow-auto">
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
                {filteredConsultants.map((consultant) => (
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
        </Card>
      )}
      
      {/* Modal de création de consultant */}
      <CreateConsultantModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSuccess={() => {
          // Fermer simplement le modal - useConsultants invalidera la requête automatiquement
          setIsCreateModalOpen(false);
          // Pas besoin de mettre à jour filteredConsultants ici, cela sera fait par l'useEffect
        }}
        // Note: Dans une application réelle, cette valeur viendrait d'un contexte d'authentification
        companyId={1} // Entreprise actuelle simulée
      />
    </div>
  );
};

export default Consultants;
