import React, { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import {
  Search,
  Plus,
  Filter,
  Upload
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { CreateConsultantModal } from "@/features/consultants/components/CreateConsultantModal";
import { useConsultants } from "@/features/consultants/hooks/useConsultants";
import { ConsultantDisplay, AvailabilityStatus } from "@/features/consultants/types";
import { Section } from "@/features/consultants/components/Section";
import { ConsultantTable } from "@/features/consultants/components/ConsultantTable";

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

  // Séparer les consultants en 4 groupes selon leur statut
  const processCandidates = useMemo(() => {
    return filteredConsultants.filter(c => c.status === "En cours de process");
  }, [filteredConsultants]);

  const qualifiedConsultants = useMemo(() => {
    return filteredConsultants.filter(c =>
      c.status === "Qualifié" ||
      c.status === "Disponible" ||
      c.status === "Partiellement disponible" ||
      c.status === "Indisponible"
    );
  }, [filteredConsultants]);

  const onMissionConsultants = useMemo(() => {
    return filteredConsultants.filter(c =>
      c.status === "En mission" ||
      c.status === "Mission"
    );
  }, [filteredConsultants]);

  const intercontractConsultants = useMemo(() => {
    return filteredConsultants.filter(c => c.status === "Intercontrat");
  }, [filteredConsultants]);

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
            Ajouter un Talent
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
        <div className="space-y-12">
          <Section title="Candidats en cours de process">
            <ConsultantTable consultants={processCandidates} />
          </Section>
          
          <Section title="Candidats qualifiés (Vivier de consultants)">
            <ConsultantTable consultants={qualifiedConsultants} />
          </Section>
          
          <Section title="Consultants en mission">
            <ConsultantTable consultants={onMissionConsultants} />
          </Section>
          
          <Section title="Consultants en intercontrat">
            <ConsultantTable consultants={intercontractConsultants} />
          </Section>
        </div>
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
