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

  // Séparer les consultants en 4 groupes selon leur statut - Adapté aux nouveaux statuts
  const processCandidates = useMemo(() => {
    return filteredConsultants.filter(c =>
      c.status === "En création" ||
      c.status === "En cours de process"
    );
  }, [filteredConsultants]);

  // Liste des consultants qualifiés triés par disponibilité
  const qualifiedConsultants = useMemo(() => {
    // Filtrer tous les consultants qualifiés
    const qualified = filteredConsultants.filter(c =>
      c.status === "Qualifié" ||
      c.status === "Qualifié - Disponible" ||
      c.status === "Bientôt disponible" ||
      c.status === "Disponible"
    );
    
    // Trier selon la date de disponibilité (croissante)
    return qualified.sort((a, b) => {
      // Si les deux n'ont pas de date, pas de tri spécifique
      if (!a.availabilityDate && !b.availabilityDate) return 0;
      
      // Si l'un n'a pas de date, il va en dernier
      if (!a.availabilityDate) return 1;
      if (!b.availabilityDate) return -1;
      
      // Tri par date croissante pour voir les prochains disponibles en premier
      return new Date(a.availabilityDate).getTime() - new Date(b.availabilityDate).getTime();
    });
  }, [filteredConsultants]);

  const onMissionConsultants = useMemo(() => {
    return filteredConsultants.filter(c => c.status === "En mission");
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
          <Button onClick={() => navigate("/consultants/create")}>
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
        // Grille 2x2 pour desktop, colonne unique pour mobile
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Section
            title="Candidats en cours de process"
            count={processCandidates.length}
          >
            <ConsultantTable consultants={processCandidates} />
          </Section>
          
          <Section
            title="Candidats qualifiés (Vivier de consultants)"
            count={qualifiedConsultants.length}
          >
            <ConsultantTable consultants={qualifiedConsultants} />
          </Section>
          
          <Section
            title="Consultants en mission"
            count={onMissionConsultants.length}
          >
            <ConsultantTable consultants={onMissionConsultants} />
          </Section>
          
          <Section
            title="Consultants en intercontrat"
            count={intercontractConsultants.length}
          >
            <ConsultantTable consultants={intercontractConsultants} />
          </Section>
        </div>
      )}
      
    </div>
  );
};

export default Consultants;
